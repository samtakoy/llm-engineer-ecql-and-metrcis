"""Метрики оценки ответов модели на ECQL.

Метрики:
- синтаксис - ответ разбирается по грамматике;
- логика - смысл совпал с эталоном, порядок условий не важен; складывается из
  пяти частей: сущность, поля, операторы, значения, суффикс вывода;
- галлюцинации - чужой язык запросов или поле вне схемы;
- строка - посимвольное совпадение с эталоном.

`self_check` подаёт эталоны вместо ответов: идеальный прогон обязан дать
единицу по всем метрикам, кроме галлюцинаций.
"""

import re
from dataclasses import dataclass

from ecql_dataset.ecql.grammar import EcqlError, Query, parse
from ecql_dataset.ecql.schema import entity_by_name

# Слова чужих языков запросов.
FOREIGN_KEYWORDS = ("SELECT", "FROM", "INSERT", "UPDATE", "DELETE", "JOIN", "GROUP BY")

FOREIGN_PATTERN = re.compile("|".join(FOREIGN_KEYWORDS))


@dataclass(frozen = True)
class Verdict:
    """Разбор одного ответа модели.

    Аргументы:
        syntax: ответ разобрался по грамматике.
        entity: сущность совпала с эталонной.
        fields: набор полей совпал.
        operators: операторы совпали.
        values: значения совпали.
        suffix: суффикс вывода совпал.
        hallucination: ответ на чужом языке или с полем вне схемы.
        exact: строка совпала с эталоном посимвольно.
        reason: чем плох ответ; пустая строка, если всё в порядке.
    """

    syntax: bool
    entity: bool
    fields: bool
    operators: bool
    values: bool
    suffix: bool
    hallucination: bool
    exact: bool
    reason: str

    @property
    def logic(self) -> bool:
        """Смысл совпал с эталоном: сущность, поля, операторы, значения, суффикс."""
        return self.entity and self.fields and self.operators and self.values and self.suffix


# Части запроса, из которых складывается логическая точность.
LOGIC_PARTS = ("entity", "fields", "operators", "values", "suffix")

# Как часть называется в отчёте.
PART_NAMES = {
    "entity": "сущность",
    "fields": "поля",
    "operators": "операторы",
    "values": "значения",
    "suffix": "суффикс",
}


def failed(*, syntax: bool, hallucination: bool, exact: bool, reason: str) -> Verdict:
    """Собирает вердикт для ответа, который дальше сравнивать нечего.

    Аргументы:
        syntax: разобрался ли ответ по грамматике.
        hallucination: чужой язык или поле вне схемы.
        exact: строка совпала с эталоном.
        reason: чем плох ответ.

    Возвращает:
        Вердикт со всеми частями смысла в False.
    """
    return Verdict(
        syntax = syntax,
        entity = False,
        fields = False,
        operators = False,
        values = False,
        suffix = False,
        hallucination = hallucination,
        exact = exact,
        reason = reason,
    )


def known_fields(*, entity: str) -> set[str] | None:
    """Возвращает имена полей сущности.

    Аргументы:
        entity: имя сущности без квадратных скобок.

    Возвращает:
        Множество имён полей; None, если сущности нет в схеме.
    """
    try:
        specification = entity_by_name(name = entity)
    except KeyError:
        return None
    return {field.name for field in specification.fields}


def compare(*, prediction: Query, reference: Query) -> dict[str, bool]:
    """Сравнивает разобранные запросы по частям.

    Порядок условий не важен: условия сводятся к множествам.

    Аргументы:
        prediction: разобранный ответ модели.
        reference: разобранный эталон.

    Возвращает:
        Соответствие «часть запроса - совпала ли».
    """
    def parts_of(query: Query) -> tuple[set, set, set]:
        fields = {condition.field for condition in query.conditions}
        operators = {(condition.field, condition.operator) for condition in query.conditions}
        values = {
            (condition.field, condition.operator, condition.value)
            for condition in query.conditions
        }
        return fields, operators, values

    predicted_fields, predicted_operators, predicted_values = parts_of(prediction)
    expected_fields, expected_operators, expected_values = parts_of(reference)
    return {
        "entity": prediction.entity == reference.entity,
        "fields": predicted_fields == expected_fields,
        "operators": predicted_operators == expected_operators,
        "values": predicted_values == expected_values,
        "suffix": prediction.suffix == reference.suffix,
    }


def judge(*, prediction: str, reference: str) -> Verdict:
    """Сравнивает ответ модели с эталоном.

    Аргументы:
        prediction: ответ модели.
        reference: эталонная строка ECQL.

    Возвращает:
        Разбор ответа.
    """
    prediction = prediction.strip()
    exact = prediction == reference.strip()

    try:
        parsed = parse(query = prediction)
    except EcqlError as error:
        foreign = FOREIGN_PATTERN.search(prediction.upper()) is not None
        return failed(
            syntax = False,
            hallucination = foreign,
            exact = exact,
            reason = f"чужой язык запросов: {error}" if foreign else str(error),
        )

    known = known_fields(entity = parsed.entity)
    if known is None:
        return failed(
            syntax = True,
            hallucination = True,
            exact = exact,
            reason = f"сущности [{parsed.entity}] нет в схеме",
        )

    unknown = [
        condition.field for condition in parsed.conditions if condition.field not in known
    ]
    if unknown:
        return failed(
            syntax = True,
            hallucination = True,
            exact = exact,
            reason = f"поля нет у [{parsed.entity}]: {' '.join(unknown)}",
        )

    expected = parse(query = reference)
    parts = compare(prediction = parsed, reference = expected)
    broken = [PART_NAMES[name] for name in LOGIC_PARTS if not parts[name]]
    return Verdict(
        syntax = True,
        hallucination = False,
        exact = exact,
        reason = "" if not broken else "не совпало: " + ", ".join(broken),
        **parts,
    )


def score(*, verdicts: list[Verdict]) -> dict[str, float]:
    """Считает доли по разобранным ответам.

    Аргументы:
        verdicts: разборы ответов.

    Возвращает:
        Доли по каждой метрике; нули на пустом списке.
    """
    names = ["синтаксис", "логика", *PART_NAMES.values(), "галлюцинации", "строка"]
    if not verdicts:
        return {name: 0.0 for name in names} | {"ответов": 0}

    total = len(verdicts)
    result = {
        "синтаксис": sum(verdict.syntax for verdict in verdicts) / total,
        "логика": sum(verdict.logic for verdict in verdicts) / total,
    }
    for part in LOGIC_PARTS:
        result[PART_NAMES[part]] = sum(getattr(verdict, part) for verdict in verdicts) / total
    result["галлюцинации"] = sum(verdict.hallucination for verdict in verdicts) / total
    result["строка"] = sum(verdict.exact for verdict in verdicts) / total
    result["ответов"] = total
    return result


def evaluate(*, records: list[dict], predictions: list[str]) -> tuple[dict, list[Verdict]]:
    """Оценивает прогон целиком.

    Аргументы:
        records: строки датасета с полями `output` и `meta`.
        predictions: ответы модели в том же порядке.

    Возвращает:
        Сводные доли и разбор каждого ответа.
    """
    if len(records) != len(predictions):
        raise ValueError(f"ответов {len(predictions)}, а строк {len(records)}")
    verdicts = [
        judge(prediction = prediction, reference = record["output"])
        for record, prediction in zip(records, predictions)
    ]
    return score(verdicts = verdicts), verdicts


def by_axis(*, records: list[dict], verdicts: list[Verdict], axis: str) -> dict[str, dict]:
    """Разбивает метрики по значениям одной оси.

    Аргументы:
        records: строки датасета.
        verdicts: разборы ответов в том же порядке.
        axis: ключ из `meta`; список значений разносится по каждому.

    Возвращает:
        Соответствие «значение оси - доли».
    """
    grouped: dict[str, list[Verdict]] = {}
    for record, verdict in zip(records, verdicts):
        value = record["meta"][axis]
        values = value if isinstance(value, list) else [value]
        for item in values:
            grouped.setdefault(str(item), []).append(verdict)
    return {value: score(verdicts = group) for value, group in sorted(grouped.items())}


def self_check(*, records: list[dict]) -> dict[str, float]:
    """Проверяет сам эвалюатор на эталонах.

    Аргументы:
        records: строки датасета.

    Возвращает:
        Доли идеального прогона.
    """
    predictions = [record["output"] for record in records]
    result, _ = evaluate(records = records, predictions = predictions)
    for name in ("синтаксис", "логика", "строка"):
        if result[name] != 1.0:
            raise AssertionError(f"самопроверка не прошла: {name} = {result[name]}")
    if result["галлюцинации"] != 0.0:
        raise AssertionError(f"самопроверка не прошла: галлюцинации = {result['галлюцинации']}")
    return result
