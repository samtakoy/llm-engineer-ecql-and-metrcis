"""Планировщик слотов датасета ECQL.

Выдаёт заданное число слотов так, чтобы квоты по осям выполнялись по
построению. Значения условий берутся из одной реальной строки таблицы, поэтому
сочетание полей заведомо существует в данных, а числовые пороги попадают в
живой диапазон. Слот содержит готовую строку ECQL; вопрос на русском пишется
человеком поверх слота.

Запуск:
    python -m ecql_dataset.build.planner \\
        --vocabulary dataset/ecql/source/vocabulary.json \\
        --output dataset/ecql/source/slots.json
"""

import argparse
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from ecql_dataset.ecql.schema import ENTITIES, EntitySpec, FieldSpec, entity_by_name

# Сколько слотов планируется всего.
TOTAL_SLOTS = 260

# Сколько слотов приходится на каждую сущность.
SLOTS_BY_ENTITY = {
    "PLACES": 95,
    "REVIEWS": 65,
    "FARES": 45,
    "PROXIMITY": 55,
}

# Сколько слотов приходится на каждое число условий в запросе.
SLOTS_BY_CONDITION_COUNT = {1: 52, 2: 88, 3: 78, 4: 42}

# Сколько слотов приходится на каждый суффикс вывода.
SLOTS_BY_SUFFIX = {None: 187, "AS LIST": 31, "AS TABLE": 26, "AS JSON": 16}

# Сколько слотов строится на связке «или».
SLOTS_WITH_OR = 25

# Сколько слотов содержат диапазон: числовое поле дважды, ABOVE и BELOW.
SLOTS_WITH_RANGE = 20

# Нижняя граница числа вхождений для каждого оператора.
MINIMUM_OPERATOR_USES = 20

# Нижняя граница числа вхождений для каждого поля.
MINIMUM_FIELD_USES = 15

# Нижняя граница числа вхождений для каждого значения перечислимого поля.
MINIMUM_VALUE_USES = 5

# Поля, для которых отрицание не имеет смысла в вопросе человека: «всё, кроме
# одного конкретного объекта» никто не спрашивает.
FIELDS_WITHOUT_NEGATION = frozenset({"@name"})

ALL_OPERATORS = ("IS", "NOT", "ABOVE", "BELOW", "CONTAINS", "NOT CONTAINS")

# Во сколько шагов округления укладывается ширина диапазона.
RANGE_WIDTH_STEPS = (2, 3, 5, 10)

# Сколько проходов починки квот делать после основной раскладки.
REPAIR_PASSES = 20

# Сколько зёрен перебрать в поисках раскладки без нарушений квот.
SEED_ATTEMPTS = 120

SEED = 42


@dataclass
class Condition:
    """Одно условие запроса.

    Аргументы:
        field: имя поля вместе с префиксом.
        operator: оператор сравнения или вхождения.
        value: значение как оно попадёт в запрос.
    """

    field: str
    operator: str
    value: str


@dataclass
class Slot:
    """Спецификация одной будущей пары датасета.

    Аргументы:
        index: порядковый номер слота.
        entity: имя сущности без квадратных скобок.
        conditions: условия запроса.
        connective: связка между условиями; None у запроса из одного условия.
        suffix: суффикс вывода; None если формат не назван.
        has_range: содержит ли слот диапазон по числовому полю.
        source_row: строка датасета, из которой взяты значения.
        ecql: готовая строка запроса.
    """

    index: int
    entity: str
    conditions: list[Condition]
    connective: str | None
    suffix: str | None
    has_range: bool
    source_row: dict
    ecql: str


def nice_step(*, value: int) -> int:
    """Подбирает шаг округления порога под порядок величины.

    Аргументы:
        value: значение из данных.

    Возвращает:
        Шаг округления.
    """
    magnitude = abs(value)
    if magnitude < 20:
        return 1
    if magnitude < 200:
        return 10
    if magnitude < 2000:
        return 100
    return 1000


def threshold_below(*, value: int) -> int:
    """Возвращает круглый порог, который значение не превышает.

    Аргументы:
        value: значение из данных.

    Возвращает:
        Порог строго больше значения.
    """
    step = nice_step(value = value)
    return (value // step + 1) * step


def threshold_above(*, value: int) -> int:
    """Возвращает круглый порог, который значение превышает.

    Аргументы:
        value: значение из данных.

    Возвращает:
        Порог строго меньше значения.
    """
    step = nice_step(value = value)
    threshold = (value // step) * step
    return threshold - step if threshold >= value else threshold


def render_condition(*, field: FieldSpec, condition: Condition) -> str:
    """Записывает условие так, как оно выглядит в запросе.

    Аргументы:
        field: описание поля.
        condition: условие.

    Возвращает:
        Строку вида «@поле ОПЕРАТОР значение».
    """
    value = condition.value if field.value_format == "bare" else f"'{condition.value}'"
    return f"{condition.field} {condition.operator} {value}"


def render_ecql(
    *,
    entity: EntitySpec,
    conditions: list[Condition],
    connective: str | None,
    suffix: str | None,
) -> str:
    """Собирает строку запроса из условий.

    Аргументы:
        entity: описание сущности.
        conditions: условия запроса.
        connective: связка между условиями.
        suffix: суффикс вывода.

    Возвращает:
        Строку ECQL.
    """
    field_by_name = {field.name: field for field in entity.fields}
    parts = [
        render_condition(field = field_by_name[condition.field], condition = condition)
        for condition in conditions
    ]
    joined = f" {connective} ".join(parts) if connective else parts[0]
    query = f"FETCH [{entity.name}] WHERE {joined}"
    return f"{query} {suffix}" if suffix else query


def numeric_bounds(*, enum_values: list[str]) -> tuple[int, int] | None:
    """Возвращает границы поля, если его перечень состоит из чисел.

    Аргументы:
        enum_values: перечень значений поля.

    Возвращает:
        Пару «минимум, максимум» или None, если поле не перечень чисел.
    """
    if not enum_values or not all(value.lstrip("-").isdigit() for value in enum_values):
        return None
    numbers = [int(value) for value in enum_values]
    return min(numbers), max(numbers)


def operator_fits_row(*, field: FieldSpec, operator: str, row: dict, enum_values: list[str]) -> bool:
    """Проверяет, применим ли оператор к значению поля в этой строке.

    Порог должен оставлять строку в выдаче: «дешевле пятисот» имеет смысл,
    только если цена меньше пятисот. Для вхождения нужен хотя бы один аспект в
    строке, для отрицания вхождения - хотя бы один аспект вне строки.

    Аргументы:
        field: описание поля.
        operator: проверяемый оператор.
        row: строка датасета.
        enum_values: полный перечень значений поля.

    Возвращает:
        True, если оператор применим.
    """
    value = row.get(field.name)
    if value is None:
        return False

    if operator == "CONTAINS":
        return isinstance(value, list) and len(value) > 0
    if operator == "NOT CONTAINS":
        return isinstance(value, list) and len(set(enum_values) - set(value)) > 0
    if operator == "IS":
        return not isinstance(value, list)
    if operator == "NOT":
        # Отрицание берёт чужое значение: иначе строка выпадает из своей же выдачи.
        return not isinstance(value, list) and len(set(enum_values) - {str(value)}) > 0
    if not str(value).lstrip("-").isdigit():
        return False

    # У поля с перечнем чисел, например оценки, порог не должен выходить за
    # границы: «оценка ниже шести» - условие, истинное всегда.
    bounds = numeric_bounds(enum_values = enum_values)
    number = int(value)
    if operator == "ABOVE":
        threshold = threshold_above(value = number)
        return threshold > 0 and (bounds is None or threshold >= bounds[0])
    if operator == "BELOW":
        threshold = threshold_below(value = number)
        return bounds is None or threshold <= bounds[1]
    return False


def build_condition(
    *,
    field: FieldSpec,
    operator: str,
    row: dict,
    enum_values: list[str],
    generator: random.Random,
) -> Condition:
    """Строит условие по строке датасета.

    Аргументы:
        field: описание поля.
        operator: оператор условия.
        row: строка датасета.
        enum_values: полный перечень значений поля.
        generator: источник случайности.

    Возвращает:
        Условие с конкретным значением.
    """
    value = row[field.name]

    if operator == "CONTAINS":
        return Condition(field = field.name, operator = operator, value = generator.choice(value))
    if operator == "NOT CONTAINS":
        absent = sorted(set(enum_values) - set(value))
        return Condition(field = field.name, operator = operator, value = generator.choice(absent))
    if operator == "NOT":
        absent = sorted(set(enum_values) - {str(value)})
        return Condition(field = field.name, operator = operator, value = generator.choice(absent))
    if operator == "ABOVE":
        return Condition(
            field = field.name,
            operator = operator,
            value = str(threshold_above(value = int(value))),
        )
    if operator == "BELOW":
        return Condition(
            field = field.name,
            operator = operator,
            value = str(threshold_below(value = int(value))),
        )
    return Condition(field = field.name, operator = operator, value = str(value))


def build_range_conditions(
    *,
    field: FieldSpec,
    row: dict,
    generator: random.Random,
) -> list[Condition]:
    """Строит пару условий диапазона вокруг значения строки.

    Границы разводятся на несколько шагов округления: «от двух до пяти тысяч»
    человек спрашивает, «от двадцати трёх до двадцати четырёх» - нет.

    Аргументы:
        field: числовое поле.
        row: строка датасета.
        generator: источник случайности.

    Возвращает:
        Условия ABOVE и BELOW, между которыми лежит значение строки.
    """
    value = int(row[field.name])
    step = nice_step(value = value)
    lower = (value // step) * step
    if lower >= value:
        lower -= step
    lower = max(lower, 0)

    width = step * generator.choice(RANGE_WIDTH_STEPS)
    upper = lower + width
    while upper <= value:
        upper += step

    return [
        Condition(field = field.name, operator = "ABOVE", value = str(lower)),
        Condition(field = field.name, operator = "BELOW", value = str(upper)),
    ]


def expand_quota(*, quota: dict) -> list:
    """Разворачивает квоту в список значений нужной длины.

    Аргументы:
        quota: соответствие «значение - сколько раз».

    Возвращает:
        Плоский список.
    """
    expanded: list = []
    for value, count in quota.items():
        expanded.extend([value] * count)
    return expanded


class QuotaTracker:
    """Считает израсходованные квоты и подсказывает, где дефицит."""

    def __init__(self) -> None:
        """Готовит пустые счётчики."""
        self.field_uses: dict[str, int] = {}
        self.operator_uses: dict[str, int] = {}
        self.value_uses: dict[tuple[str, str, str], int] = {}

    def register(self, *, entity_name: str, condition: Condition) -> None:
        """Учитывает одно условие.

        Аргументы:
            entity_name: имя сущности.
            condition: условие.
        """
        self.field_uses[condition.field] = self.field_uses.get(condition.field, 0) + 1
        self.operator_uses[condition.operator] = self.operator_uses.get(condition.operator, 0) + 1
        key = (entity_name, condition.field, condition.value)
        self.value_uses[key] = self.value_uses.get(key, 0) + 1

    def field_deficit(self, *, field_name: str) -> int:
        """Возвращает недобор по полю.

        Аргументы:
            field_name: имя поля.

        Возвращает:
            Сколько вхождений не хватает до порога.
        """
        return max(0, MINIMUM_FIELD_USES - self.field_uses.get(field_name, 0))

    def operator_deficit(self, *, operator: str) -> int:
        """Возвращает недобор по оператору.

        Аргументы:
            operator: оператор.

        Возвращает:
            Сколько вхождений не хватает до порога.
        """
        return max(0, MINIMUM_OPERATOR_USES - self.operator_uses.get(operator, 0))

    def value_deficit(self, *, entity_name: str, field_name: str, value: str) -> int:
        """Возвращает недобор по конкретному значению поля.

        Аргументы:
            entity_name: имя сущности.
            field_name: имя поля.
            value: значение.

        Возвращает:
            Сколько вхождений не хватает до порога.
        """
        key = (entity_name, field_name, value)
        return max(0, MINIMUM_VALUE_USES - self.value_uses.get(key, 0))


def row_score(
    *,
    entity: EntitySpec,
    entity_name: str,
    row: dict,
    tracker: QuotaTracker,
    needs_name: bool,
    needs_numeric: bool,
) -> int:
    """Оценивает, насколько строка закрывает текущий дефицит квот.

    Аргументы:
        entity: описание сущности.
        entity_name: имя сущности.
        row: строка датасета.
        tracker: счётчики квот.
        needs_name: нужна ли строка с пригодным для вопроса именем.
        needs_numeric: нужно ли числовое поле в строке.

    Возвращает:
        Оценку; отрицательная означает, что строка не подходит.
    """
    if needs_name and not row.get("name_askable"):
        return -1
    if needs_numeric and not any(
        field.kind == "number" and field.name in row for field in entity.fields
    ):
        return -1

    score = 0
    for field in entity.fields:
        value = row.get(field.name)
        if value is None:
            continue
        score += tracker.field_deficit(field_name = field.name)
        values = value if isinstance(value, list) else [value]
        for item in values:
            score += 3 * tracker.value_deficit(
                entity_name = entity_name,
                field_name = field.name,
                value = str(item),
            )
    return score


def pick_row(
    *,
    entity: EntitySpec,
    entity_name: str,
    samples: list[dict],
    tracker: QuotaTracker,
    needs_name: bool,
    needs_numeric: bool,
    generator: random.Random,
) -> dict:
    """Выбирает строку датасета под текущий дефицит квот.

    Аргументы:
        entity: описание сущности.
        entity_name: имя сущности.
        samples: образцы строк сущности.
        tracker: счётчики квот.
        needs_name: нужна ли строка с пригодным именем.
        needs_numeric: нужно ли числовое поле.
        generator: источник случайности.

    Возвращает:
        Выбранную строку.
    """
    scored = []
    for row in samples:
        score = row_score(
            entity = entity,
            entity_name = entity_name,
            row = row,
            tracker = tracker,
            needs_name = needs_name,
            needs_numeric = needs_numeric,
        )
        if score >= 0:
            scored.append((score, generator.random(), row))
    if not scored:
        return generator.choice(samples)
    scored.sort(key = lambda item: (-item[0], item[1]))
    top = scored[: max(1, len(scored) // 20)]
    return generator.choice(top)[2]


def choose_conditions(
    *,
    entity: EntitySpec,
    entity_name: str,
    row: dict,
    condition_count: int,
    forced: list[tuple[str, str]],
    wants_range: bool,
    enum_values: dict[str, list[str]],
    tracker: QuotaTracker,
    generator: random.Random,
) -> list[Condition]:
    """Набирает условия слота из полей выбранной строки.

    Аргументы:
        entity: описание сущности.
        entity_name: имя сущности.
        row: строка датасета.
        condition_count: сколько условий нужно.
        forced: обязательные пары «поле и значение» из очереди квот.
        wants_range: начинать ли с диапазона по числовому полю.
        enum_values: перечни значений полей.
        tracker: счётчики квот.
        generator: источник случайности.

    Возвращает:
        Условия слота.
    """
    conditions: list[Condition] = []
    used_fields: set[str] = set()
    used_operators: set[str] = set()
    field_by_name = {field.name: field for field in entity.fields}

    for field_name, value in forced:
        if field_name in used_fields or len(conditions) >= condition_count:
            continue
        operator = "CONTAINS" if field_by_name[field_name].value_format == "quoted" and isinstance(
            row.get(field_name), list
        ) else "IS"
        used_fields.add(field_name)
        used_operators.add(operator)
        conditions.append(Condition(field = field_name, operator = operator, value = value))

    if wants_range:
        numeric_fields = [
            field for field in entity.fields if field.kind == "number" and field.name in row
        ]
        if numeric_fields:
            field = generator.choice(numeric_fields)
            conditions.extend(build_range_conditions(
                field = field,
                row = row,
                generator = generator,
            ))
            used_fields.add(field.name)

    while len(conditions) < condition_count:
        candidates = []
        for field in entity.fields:
            if field.name not in row:
                continue
            is_multivalue = isinstance(row.get(field.name), list)
            if field.name in used_fields and not is_multivalue:
                continue
            # Имя берётся только у объекта, о котором человек способен спросить.
            if field.name == "@name" and not row.get("name_askable"):
                continue
            for operator in field.operators:
                if field.name in used_fields and operator in used_operators:
                    continue
                if operator in ("NOT", "NOT CONTAINS") and field.name in FIELDS_WITHOUT_NEGATION:
                    continue
                if not operator_fits_row(
                    field = field,
                    operator = operator,
                    row = row,
                    enum_values = enum_values.get(field.name, []),
                ):
                    continue
                candidate = build_condition(
                    field = field,
                    operator = operator,
                    row = row,
                    enum_values = enum_values.get(field.name, []),
                    generator = generator,
                )
                score = (
                    tracker.field_deficit(field_name = field.name)
                    + 2 * tracker.operator_deficit(operator = operator)
                    + 4 * tracker.value_deficit(
                        entity_name = entity_name,
                        field_name = field.name,
                        value = candidate.value,
                    )
                )
                candidates.append((score, generator.random(), candidate))

        if not candidates:
            break

        candidates.sort(key = lambda item: (-item[0], item[1]))
        _, _, chosen = candidates[0]
        used_fields.add(chosen.field)
        used_operators.add(chosen.operator)
        conditions.append(chosen)

    if len(conditions) >= 2 and any(
        field_by_name[condition.field].kind == "number" for condition in conditions
    ) and not any(field_by_name[condition.field].is_topic for condition in conditions):
        forced_names = {field_name for field_name, _ in forced}
        topic_candidates = [
            field for field in entity.fields
            if field.is_topic and field.name in row and not isinstance(row[field.name], list)
        ]
        replaceable = [
            position for position, condition in enumerate(conditions)
            if field_by_name[condition.field].kind != "number"
            and condition.field not in forced_names
        ]
        if topic_candidates and replaceable:
            topic = generator.choice(topic_candidates)
            conditions[replaceable[-1]] = Condition(
                field = topic.name,
                operator = "IS",
                value = str(row[topic.name]),
            )
        elif topic_candidates:
            topic = generator.choice(topic_candidates)
            conditions[-1] = Condition(
                field = topic.name,
                operator = "IS",
                value = str(row[topic.name]),
            )

    return conditions[:condition_count]


def choose_or_conditions(
    *,
    entity: EntitySpec,
    row: dict,
    samples: list[dict],
    condition_count: int,
    enum_values: dict[str, list[str]],
    generator: random.Random,
) -> list[Condition]:
    """Набирает условия слота на связке «или»: перечень вариантов по одному полю.

    Аргументы:
        entity: описание сущности.
        row: строка датасета, задающая первый вариант.
        samples: образцы строк сущности - источник остальных вариантов.
        condition_count: сколько вариантов перечислить.
        enum_values: перечни значений полей.
        generator: источник случайности.

    Возвращает:
        Условия слота.
    """
    # Перечисление не должно накрывать все значения поля: такое условие
    # истинно всегда и вопросом не выражается.
    candidates = [
        field
        for field in entity.fields
        if field.allows_enumeration
        and field.name in row
        and not isinstance(row[field.name], list)
        and len(enum_values.get(field.name, [])) != condition_count
    ]
    if not candidates:
        candidates = [
            field for field in entity.fields
            if field.allows_enumeration and field.name in row
        ]
    field = generator.choice(candidates)

    values = [str(row[field.name])]
    pool = [
        str(sample[field.name])
        for sample in samples
        if field.name in sample and str(sample[field.name]) not in values
    ]
    generator.shuffle(pool)
    for value in pool:
        if len(values) >= condition_count:
            break
        if value not in values:
            values.append(value)

    return [
        Condition(field = field.name, operator = "IS", value = value)
        for value in values[:condition_count]
    ]


def build_required_placements(*, vocabulary: dict, generator: random.Random) -> dict[str, list[tuple[str, str]]]:
    """Строит очередь обязательных значений по каждой сущности.

    Жадный отбор не добирает редкие значения: строка датасета может их вовсе не
    содержать. Поэтому обязательные значения планируются заранее, и слот берёт
    их из очереди, а не надеется встретить.

    Аргументы:
        vocabulary: содержимое vocabulary.json.
        generator: источник случайности.

    Возвращает:
        Соответствие «сущность - список пар поле и значение».
    """
    placements: dict[str, list[tuple[str, str]]] = {}
    for entity_name, entity in vocabulary["entities"].items():
        queue: list[tuple[str, str]] = []
        for field_name, described in entity["fields"].items():
            if described["kind"] != "enum":
                continue
            for value in described["values"]:
                queue.extend([(field_name, value)] * MINIMUM_VALUE_USES)
        generator.shuffle(queue)
        placements[entity_name] = queue
    return placements


def row_covers(*, row: dict, field_name: str, value: str) -> bool:
    """Проверяет, содержит ли строка нужное значение поля.

    Аргументы:
        row: строка датасета.
        field_name: имя поля.
        value: искомое значение.

    Возвращает:
        True, если значение есть в строке.
    """
    present = row.get(field_name)
    if present is None:
        return False
    if isinstance(present, list):
        return value in present
    return str(present) == value


def take_placements(
    *,
    queue: list[tuple[str, str]],
    samples: list[dict],
    limit: int,
    tracker: QuotaTracker,
    entity_name: str,
) -> tuple[list[tuple[str, str]], dict | None]:
    """Забирает из очереди значения, которые можно закрыть одной строкой.

    Аргументы:
        queue: очередь обязательных значений сущности.
        samples: образцы строк сущности.
        limit: сколько условий помещается в слот.
        tracker: счётчики квот.
        entity_name: имя сущности.

    Возвращает:
        Пару «взятые значения, подходящая строка»; строка None, если очередь
        пуста или подходящей строки нет.
    """
    while queue and tracker.value_deficit(
        entity_name = entity_name,
        field_name = queue[0][0],
        value = queue[0][1],
    ) == 0:
        queue.pop(0)

    if not queue or limit < 1:
        return [], None

    head_field, head_value = queue[0]
    matching = [row for row in samples if row_covers(row = row, field_name = head_field, value = head_value)]
    if not matching:
        queue.pop(0)
        return [], None

    taken = [queue.pop(0)]
    if limit >= 2:
        for position, (field_name, value) in enumerate(queue):
            if field_name == head_field:
                continue
            narrowed = [row for row in matching if row_covers(row = row, field_name = field_name, value = value)]
            if narrowed:
                matching = narrowed
                taken.append(queue.pop(position))
                break

    return taken, matching[0] if matching else None


def build_slots(*, vocabulary: dict, seed: int) -> list[Slot]:
    """Строит все слоты датасета с соблюдением квот.

    Аргументы:
        vocabulary: содержимое vocabulary.json.
        seed: зерно генератора случайных чисел.

    Возвращает:
        Список слотов.
    """
    generator = random.Random(seed)
    tracker = QuotaTracker()

    entity_plan = expand_quota(quota = SLOTS_BY_ENTITY)
    condition_plan = expand_quota(quota = SLOTS_BY_CONDITION_COUNT)
    suffix_plan = expand_quota(quota = SLOTS_BY_SUFFIX)
    generator.shuffle(entity_plan)
    generator.shuffle(condition_plan)
    generator.shuffle(suffix_plan)

    entities_with_numbers = {
        entity.name for entity in ENTITIES if any(field.kind == "number" for field in entity.fields)
    }

    # Связка «или» и диапазоны требуют минимум двух условий, диапазон - ещё и
    # числового поля у сущности.
    multi_condition_indices = [index for index, count in enumerate(condition_plan) if count >= 2]
    range_capable_indices = [index for index, count in enumerate(condition_plan) if count >= 3]
    generator.shuffle(multi_condition_indices)
    or_indices = set(multi_condition_indices[:SLOTS_WITH_OR])
    range_indices = set(
        index
        for index in range_capable_indices
        if index not in or_indices and entity_plan[index] in entities_with_numbers
    )
    range_indices = set(sorted(range_indices)[:SLOTS_WITH_RANGE])

    required = build_required_placements(vocabulary = vocabulary, generator = generator)

    slots: list[Slot] = []
    for index in range(TOTAL_SLOTS):
        entity_name = entity_plan[index]
        entity = entity_by_name(name = entity_name)
        entity_vocabulary = vocabulary["entities"][entity_name]
        samples = entity_vocabulary["samples"]
        enum_values = {
            field_name: described.get("values", [])
            for field_name, described in entity_vocabulary["fields"].items()
        }

        condition_count = condition_plan[index]
        suffix = suffix_plan[index]
        wants_or = index in or_indices
        wants_range = index in range_indices

        has_name_field = any(field.name == "@name" for field in entity.fields)
        needs_name = has_name_field and tracker.field_deficit(field_name = "@name") > 0

        forced: list[tuple[str, str]] = []
        row = None
        placement_limit = condition_count - 2 if wants_range else condition_count
        if not wants_or and placement_limit >= 1:
            candidate_rows = [
                sample for sample in samples
                if not needs_name or sample.get("name_askable")
            ] or samples
            forced, row = take_placements(
                queue = required[entity_name],
                samples = candidate_rows,
                limit = placement_limit,
                tracker = tracker,
                entity_name = entity_name,
            )

        if row is None or (wants_range and not any(
            field.kind == "number" and field.name in row for field in entity.fields
        )):
            forced = []
            row = pick_row(
                entity = entity,
                entity_name = entity_name,
                samples = samples,
                tracker = tracker,
                needs_name = needs_name,
                needs_numeric = wants_range,
                generator = generator,
            )

        if wants_or:
            conditions = choose_or_conditions(
                entity = entity,
                row = row,
                samples = samples,
                condition_count = condition_count,
                enum_values = enum_values,
                generator = generator,
            )
            connective = "||"
        else:
            conditions = choose_conditions(
                entity = entity,
                entity_name = entity_name,
                row = row,
                condition_count = condition_count,
                forced = forced,
                wants_range = wants_range,
                enum_values = enum_values,
                tracker = tracker,
                generator = generator,
            )
            connective = "&&" if len(conditions) > 1 else None

        for condition in conditions:
            tracker.register(entity_name = entity_name, condition = condition)

        slots.append(Slot(
            index = index + 1,
            entity = entity_name,
            conditions = conditions,
            connective = connective,
            suffix = suffix,
            has_range = wants_range and len(conditions) >= 2,
            source_row = row,
            ecql = render_ecql(
                entity = entity,
                conditions = conditions,
                connective = connective,
                suffix = suffix,
            ),
        ))

    return slots


def survives_removal(
    *,
    tracker: QuotaTracker,
    entity_name: str,
    condition: Condition,
    enum_fields: set[str],
) -> bool:
    """Проверяет, что удаление условия не опустит ни одну квоту ниже порога.

    Аргументы:
        tracker: счётчики квот.
        entity_name: имя сущности.
        condition: условие-кандидат на удаление.
        enum_fields: поля с перечислимыми значениями.

    Возвращает:
        True, если условие можно заменить безболезненно.
    """
    if tracker.field_uses.get(condition.field, 0) - 1 < MINIMUM_FIELD_USES:
        return False
    if tracker.operator_uses.get(condition.operator, 0) - 1 < MINIMUM_OPERATOR_USES:
        return False
    if condition.field in enum_fields:
        key = (entity_name, condition.field, condition.value)
        if tracker.value_uses.get(key, 0) - 1 < MINIMUM_VALUE_USES:
            return False
    return True


def repair_deficits(*, slots: list[Slot], vocabulary: dict, generator: random.Random) -> None:
    """Добирает оставшиеся квоты заменой избыточных условий.

    Основной проход раскладывает обязательные значения по очереди, но часть
    квот может остаться незакрытой: подходящая строка не встретилась вовремя.
    Проход починки заменяет условия, чьи значения уже набрали запас, на
    недостающие - и только там, где строка слота это допускает.

    Аргументы:
        slots: построенные слоты; изменяются на месте.
        vocabulary: содержимое vocabulary.json.
        generator: источник случайности.
    """
    for _ in range(REPAIR_PASSES):
        tracker = QuotaTracker()
        for slot in slots:
            for condition in slot.conditions:
                tracker.register(entity_name = slot.entity, condition = condition)

        deficits: list[tuple[str, str, str, str]] = []
        for entity_name, entity in vocabulary["entities"].items():
            for field_name, described in entity["fields"].items():
                if described["kind"] != "enum":
                    continue
                multivalue = described.get("multivalue", False)
                for value in described["values"]:
                    if tracker.value_deficit(
                        entity_name = entity_name,
                        field_name = field_name,
                        value = value,
                    ) > 0:
                        operator = "CONTAINS" if multivalue else "IS"
                        deficits.append((entity_name, field_name, value, operator))

        for operator in ("NOT CONTAINS", "CONTAINS"):
            shortfall = tracker.operator_deficit(operator = operator)
            for _ in range(shortfall):
                deficits.append(("REVIEWS", "@aspects", "", operator))

        if not deficits:
            return

        repaired = False
        for entity_name, field_name, value, operator in deficits:
            candidates = [
                slot for slot in slots
                if slot.entity == entity_name
                and slot.connective != "||"
                and len(slot.conditions) >= 2
            ]
            generator.shuffle(candidates)
            for slot in candidates:
                multivalue = vocabulary["entities"][entity_name]["fields"][field_name].get("multivalue", False)
                if not multivalue and any(c.field == field_name for c in slot.conditions):
                    continue
                enum_values = vocabulary["entities"][entity_name]["fields"][field_name].get("values", [])
                if operator == "NOT CONTAINS":
                    present = slot.source_row.get(field_name)
                    if not isinstance(present, list):
                        continue
                    absent = sorted(set(enum_values) - set(present))
                    if not absent:
                        continue
                    replacement = Condition(field = field_name, operator = operator, value = absent[0])
                elif not row_covers(row = slot.source_row, field_name = field_name, value = value):
                    continue
                else:
                    replacement = Condition(field = field_name, operator = operator, value = value)

                signature = (replacement.field, replacement.operator, replacement.value)
                if any((c.field, c.operator, c.value) == signature for c in slot.conditions):
                    continue

                enum_fields = {
                    name for name, described in vocabulary["entities"][entity_name]["fields"].items()
                    if described["kind"] == "enum"
                }
                expendable = [
                    position for position, condition in enumerate(slot.conditions)
                    if condition.field != field_name
                    and survives_removal(
                        tracker = tracker,
                        entity_name = entity_name,
                        condition = condition,
                        enum_fields = enum_fields,
                    )
                ]
                if not expendable:
                    continue

                previous = slot.conditions[expendable[-1]]
                slot.conditions[expendable[-1]] = replacement
                rebuilt_ecql = render_ecql(
                    entity = entity_by_name(name = entity_name),
                    conditions = slot.conditions,
                    connective = slot.connective,
                    suffix = slot.suffix,
                )
                if rebuilt_ecql in {other.ecql for other in slots if other is not slot}:
                    slot.conditions[expendable[-1]] = previous
                    continue
                slot.ecql = render_ecql(
                    entity = entity_by_name(name = entity_name),
                    conditions = slot.conditions,
                    connective = slot.connective,
                    suffix = slot.suffix,
                )
                repaired = True
                break

        if not repaired:
            return


def report_quotas(*, slots: list[Slot], vocabulary: dict) -> list[str]:
    """Проверяет выполнение квот и возвращает список нарушений.

    Аргументы:
        slots: построенные слоты.
        vocabulary: содержимое vocabulary.json.

    Возвращает:
        Список сообщений о нарушениях; пустой, если всё сошлось.
    """
    problems: list[str] = []
    tracker = QuotaTracker()
    for slot in slots:
        for condition in slot.conditions:
            tracker.register(entity_name = slot.entity, condition = condition)

    for operator in ALL_OPERATORS:
        uses = tracker.operator_uses.get(operator, 0)
        if uses < MINIMUM_OPERATOR_USES:
            problems.append(f"оператор {operator}: {uses} из {MINIMUM_OPERATOR_USES}")

    reported_fields: set[str] = set()
    for entity in ENTITIES:
        for field in entity.fields:
            uses = tracker.field_uses.get(field.name, 0)
            if uses < MINIMUM_FIELD_USES and field.name not in reported_fields:
                reported_fields.add(field.name)
                problems.append(f"поле {field.name}: {uses} из {MINIMUM_FIELD_USES}")

    for entity_name, entity in vocabulary["entities"].items():
        for field_name, described in entity["fields"].items():
            if described["kind"] != "enum":
                continue
            for value in described["values"]:
                uses = tracker.value_uses.get((entity_name, field_name, value), 0)
                if uses < MINIMUM_VALUE_USES:
                    problems.append(
                        f"значение {entity_name}.{field_name} = {value}: {uses} из {MINIMUM_VALUE_USES}"
                    )

    counted_range = sum(slot.has_range for slot in slots)
    if counted_range < SLOTS_WITH_RANGE:
        problems.append(f"слотов с диапазоном: {counted_range} из {SLOTS_WITH_RANGE}")

    for slot in slots:
        signatures = {
            (condition.field, condition.operator, condition.value)
            for condition in slot.conditions
        }
        if len(slot.conditions) != len(signatures):
            problems.append(f"слот {slot.index}: повтор условия")

    return problems


def deduplicate(*, slots: list[Slot], vocabulary: dict, generator: random.Random) -> int:
    """Разводит слоты с одинаковой строкой запроса.

    Одинаковый ECQL в двух парах - это дубликат обучающего примера: он тратит
    место и перекашивает вес шаблона. Повторы пересобираются из другой строки
    датасета с тем же набором полей и операторов.

    Аргументы:
        slots: построенные слоты; изменяются на месте.
        vocabulary: содержимое vocabulary.json.
        generator: источник случайности.

    Возвращает:
        Сколько дубликатов осталось неразведёнными.
    """
    seen: set[str] = set()
    remaining = 0

    for slot in slots:
        if slot.ecql not in seen:
            seen.add(slot.ecql)
            continue

        entity = entity_by_name(name = slot.entity)
        entity_vocabulary = vocabulary["entities"][slot.entity]
        enum_values = {
            field_name: described.get("values", [])
            for field_name, described in entity_vocabulary["fields"].items()
        }
        field_by_name = {field.name: field for field in entity.fields}

        candidates = list(entity_vocabulary["samples"])
        generator.shuffle(candidates)

        replaced = False
        for row in candidates:
            if not all(condition.field in row for condition in slot.conditions):
                continue
            rebuilt: list[Condition] = []
            for condition in slot.conditions:
                field = field_by_name[condition.field]
                if not operator_fits_row(
                    field = field,
                    operator = condition.operator,
                    row = row,
                    enum_values = enum_values.get(field.name, []),
                ):
                    rebuilt = []
                    break
                rebuilt.append(build_condition(
                    field = field,
                    operator = condition.operator,
                    row = row,
                    enum_values = enum_values.get(field.name, []),
                    generator = generator,
                ))
            if not rebuilt:
                continue

            candidate_ecql = render_ecql(
                entity = entity,
                conditions = rebuilt,
                connective = slot.connective,
                suffix = slot.suffix,
            )
            if candidate_ecql in seen:
                continue

            slot.conditions = rebuilt
            slot.source_row = row
            slot.ecql = candidate_ecql
            seen.add(candidate_ecql)
            replaced = True
            break

        if not replaced:
            remaining += 1

    return remaining


def plan_with_seeds(*, vocabulary: dict) -> tuple[list[Slot], list[str], int]:
    """Перебирает зёрна генератора, пока все квоты не сойдутся.

    Раскладка жадная, поэтому отдельные зёрна упираются в неразрешимый остаток.
    Дешевле перебрать зерно, чем усложнять алгоритм; результат остаётся
    воспроизводимым, потому что зерно записывается в отчёт.

    Аргументы:
        vocabulary: содержимое vocabulary.json.

    Возвращает:
        Тройку «слоты, нарушения квот, использованное зерно».
    """
    best: tuple[list[Slot], list[str], int] | None = None
    for offset in range(SEED_ATTEMPTS):
        seed = SEED + offset
        slots = build_slots(vocabulary = vocabulary, seed = seed)
        deduplicate(slots = slots, vocabulary = vocabulary, generator = random.Random(seed))
        repair_deficits(slots = slots, vocabulary = vocabulary, generator = random.Random(seed))
        duplicates = deduplicate(slots = slots, vocabulary = vocabulary, generator = random.Random(seed))
        problems = report_quotas(slots = slots, vocabulary = vocabulary)
        if duplicates:
            problems.append(f"дубликатов запроса: {duplicates}")
        if not problems:
            return slots, problems, seed
        if best is None or len(problems) < len(best[1]):
            best = (slots, problems, seed)
    return best


def cli() -> None:
    """Точка входа командной строки."""
    parser = argparse.ArgumentParser(description = "планировщик слотов датасета ECQL")
    parser.add_argument("--vocabulary", required = True, type = Path, help = "словарь значений")
    parser.add_argument("--output", required = True, type = Path, help = "путь json со слотами")
    arguments = parser.parse_args()

    vocabulary = json.loads(arguments.vocabulary.read_text(encoding = "utf-8"))
    slots, problems, used_seed = plan_with_seeds(vocabulary = vocabulary)

    arguments.output.parent.mkdir(parents = True, exist_ok = True)
    arguments.output.write_text(
        json.dumps([asdict(slot) for slot in slots], ensure_ascii = False, indent = 2) + "\n",
        encoding = "utf-8",
    )

    print(f"слотов: {len(slots)}, зерно {used_seed}")
    if problems:
        print(f"нарушений квот: {len(problems)}")
        for problem in problems:
            print(f"  {problem}")
    else:
        print("квоты сошлись")
    print(f"слоты записаны: {arguments.output}")


if __name__ == "__main__":
    cli()
