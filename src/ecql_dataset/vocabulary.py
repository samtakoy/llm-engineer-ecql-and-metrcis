"""Выгрузка словаря значений ECQL из таблиц КМВ.

Читает csv соседнего проекта и складывает значения полей в один json. Дальше
планировщик, сборщик и валидатор работают только с этим json, поэтому проект
не зависит от того, где лежит датасет КМВ.

Запуск:
    python -m ecql_dataset.vocabulary \\
        --dataset-root /path/to/final_project3/packages/kmv-dataset/data/dataset \\
        --output dataset/ecql/vocabulary.json
"""

import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

from ecql_dataset.schema import (
    ENTITIES,
    MULTIVALUE_FIELDS,
    ROUTE_TYPE_TO_TRANSPORT,
    EntitySpec,
    FieldSpec,
    to_code,
)

# Сколько примеров сохранять для полей с открытым перечнем значений.
OPEN_FIELD_EXAMPLES = 12

# Сколько примеров сохранять для числовых полей.
NUMBER_FIELD_EXAMPLES = 8

# Сколько примеров сохранять для полей с именем объекта.
NAME_FIELD_EXAMPLES = 30

# Сколько строк-образцов держать на каждое значение перечислимого поля.
ROWS_PER_ENUM_VALUE = 25

# Верхняя граница числа строк-образцов у одной сущности.
MAXIMUM_SAMPLE_ROWS = 600

SAMPLE_SEED = 42


def read_table(*, table_path: Path) -> list[dict[str, str]]:
    """Читает csv в список словарей.

    Аргументы:
        table_path: путь к таблице.

    Возвращает:
        Строки таблицы.
    """
    with table_path.open(encoding = "utf-8") as table_file:
        return list(csv.DictReader(table_file))


def build_proximity_rows(*, dataset_root: Path) -> list[dict[str, str]]:
    """Собирает строки сущности PROXIMITY с производным полем имени якоря.

    Аргументы:
        dataset_root: корень датасета КМВ.

    Возвращает:
        Строки соседства, где place_id заменён именем объекта.
    """
    places = read_table(table_path = dataset_root / "places/places.csv")
    anchor_by_place = {row["place_id"]: (row["name"], row["category"]) for row in places}

    rows = []
    for row in read_table(table_path = dataset_root / "places/proximity.csv"):
        anchor = anchor_by_place.get(row["place_id"])
        if anchor is None:
            continue
        anchor_name, anchor_category = anchor
        rows.append({
            "place_id": row["place_id"],
            "name": anchor_name,
            "category": anchor_category,
            "neighbour_category": row["neighbour_category"],
            "distance_m": row["distance_m"],
        })
    return rows


def split_route_endpoints(*, route_long_name: str) -> tuple[str, str]:
    """Выделяет города отправления и прибытия из имени маршрута gtfs.

    Городской маршрут записан как «Город: остановка - остановка», у него оба
    конца совпадают с городом. Междугородний записан как «A - B», где часть
    после запятой или слэша уточняет вокзал или терминал и отбрасывается.

    Аргументы:
        route_long_name: значение route_long_name из routes.txt.

    Возвращает:
        Пару «город отправления, город прибытия».
    """
    if ": " in route_long_name:
        city_prefix, _, tail = route_long_name.partition(":")
        if " - " in tail:
            return city_prefix.strip(), city_prefix.strip()

    left, _, right = route_long_name.partition(" - ")

    def city_of(part: str) -> str:
        part = part.split(" => ")[0]
        part = part.split(",")[0]
        part = part.split(" / ")[0]
        return part.strip()

    return city_of(left), city_of(right)


def build_fares_rows(*, dataset_root: Path) -> list[dict[str, str]]:
    """Собирает строки сущности FARES с производными полями рейса.

    Аргументы:
        dataset_root: корень датасета КМВ.

    Возвращает:
        Строки цен, дополненные видом транспорта и городами маршрута.
    """
    routes = {
        row["route_id"]: row
        for row in read_table(table_path = dataset_root / "transit/gtfs/routes.txt")
    }
    trips = {
        row["trip_id"]: row
        for row in read_table(table_path = dataset_root / "transit/gtfs/trips.txt")
    }

    rows = []
    for row in read_table(table_path = dataset_root / "transit/leg_prices.csv"):
        trip = trips.get(row["trip_id"])
        if trip is None:
            continue
        route = routes[trip["route_id"]]
        route_start, route_end = split_route_endpoints(route_long_name = route["route_long_name"])
        rows.append({
            "transport": ROUTE_TYPE_TO_TRANSPORT[route["route_type"]],
            "route_start": route_start,
            "route_end": route_end,
            "fare_class": row["fare_class"],
            "price_rub": row["price_rub"],
        })
    return rows


def load_entity_rows(*, entity: EntitySpec, dataset_root: Path) -> list[dict[str, str]]:
    """Загружает строки сущности, разворачивая производные поля.

    Аргументы:
        entity: описание сущности.
        dataset_root: корень датасета КМВ.

    Возвращает:
        Строки, в которых доступны все поля сущности.
    """
    if entity.name == "PROXIMITY":
        return build_proximity_rows(dataset_root = dataset_root)
    if entity.name == "FARES":
        return build_fares_rows(dataset_root = dataset_root)
    return read_table(table_path = dataset_root / entity.table)


def column_of(*, field: FieldSpec) -> str:
    """Возвращает имя колонки, в которой лежит значение поля.

    Аргументы:
        field: описание поля.

    Возвращает:
        Имя колонки в загруженных строках сущности.
    """
    if field.column is not None:
        return field.column
    return field.name.lstrip("@")


def collect_field_values(*, field: FieldSpec, rows: list[dict[str, str]]) -> Counter:
    """Считает частоты значений поля по строкам сущности.

    Аргументы:
        field: описание поля.
        rows: строки сущности.

    Возвращает:
        Счётчик значений; пустые значения не учитываются.
    """
    column = column_of(field = field)
    counter: Counter = Counter()
    for row in rows:
        raw_value = row.get(column, "").strip()
        if not raw_value:
            continue
        if field.name in MULTIVALUE_FIELDS:
            for part in raw_value.split(","):
                part = part.strip()
                if part:
                    counter[part] += 1
        else:
            counter[to_code(field = field.name, value = raw_value)] += 1
    return counter


# Имя объекта годится для вопроса, если начинается с буквы и не слишком длинное.
NAME_PATTERN = re.compile(r"^[A-Z\u0410-\u042f\u0401]")

# Служебные записи датасета: номера станций, километровые столбы, перечисления.
NAME_REJECT_PATTERN = re.compile(r"[0-9;]")
NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 40


def is_askable_name(*, name: str) -> bool:
    """Проверяет, годится ли имя объекта для вопроса человека.

    Отсеиваются служебные записи датасета и нарицательные слова: имя должно
    начинаться с заглавной буквы, иначе «кафе» или «гостиница» попадут в поле
    имени и вступят в противоречие с категорией объекта.

    Аргументы:
        name: имя объекта.

    Возвращает:
        True, если имя пригодно.
    """
    return (
        NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH
        and NAME_PATTERN.match(name) is not None
        and NAME_REJECT_PATTERN.search(name) is None
    )


def stable_order_key(*, value: str) -> str:
    """Возвращает воспроизводимый ключ перемешивания.

    Сортировка по алфавиту сгоняет в начало списка имена на латинице и в
    кавычках. Хеш даёт тот же порядок при каждом запуске, но без такого перекоса.

    Аргументы:
        value: значение для упорядочивания.

    Возвращает:
        Ключ сортировки.
    """
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def pick_unique_by_category(*, rows: list[dict[str, str]], column: str, limit: int) -> list[str]:
    """Отбирает однозначные имена объектов, поровну по категориям.

    Частотный отбор для имён не годится: наверху оказываются сетевые магазины и
    безымянные объекты, повторяющиеся десятками. Имя считается пригодным, если
    указывает ровно на один place_id - тогда запрос по нему вернёт один объект,
    а не сорок «Магнитов». Внутри категории имена идут по убыванию числа строк:
    у сущности соседства это выводит наверх объекты с большим числом соседей.

    Аргументы:
        rows: строки сущности; должны содержать place_id и category.
        column: колонка с именем.
        limit: сколько имён вернуть.

    Возвращает:
        Имена, перемешанные по категориям, не длиннее limit.
    """
    places_by_name: dict[str, set[str]] = {}
    rows_by_name: Counter = Counter()
    category_by_name: dict[str, str] = {}

    for row in rows:
        name = row.get(column, "").strip()
        category = row.get("category", "").strip()
        place_id = row.get("place_id", "").strip()
        if not name or not category or not place_id:
            continue
        places_by_name.setdefault(name, set()).add(place_id)
        rows_by_name[name] += 1
        category_by_name[name] = category

    by_category: dict[str, list[str]] = {}
    for name, place_ids in places_by_name.items():
        if len(place_ids) != 1 or not is_askable_name(name = name):
            continue
        by_category.setdefault(category_by_name[name], []).append(name)

    for names in by_category.values():
        names.sort(key = lambda name: (-rows_by_name[name], stable_order_key(value = name)))

    picked: list[str] = []
    position = 0
    while len(picked) < limit and any(position < len(names) for names in by_category.values()):
        for category in sorted(by_category):
            names = by_category[category]
            if position < len(names) and len(picked) < limit:
                picked.append(names[position])
        position += 1
    return picked


def pick_open_examples(
    *,
    field: FieldSpec,
    rows: list[dict[str, str]],
    counter: Counter,
) -> list[str]:
    """Отбирает примеры значений открытого поля по его политике.

    Аргументы:
        field: описание поля.
        rows: строки сущности.
        counter: частоты значений поля.

    Возвращает:
        Список примеров.
    """
    if field.examples_policy == "unique_by_category":
        return pick_unique_by_category(
            rows = rows,
            column = column_of(field = field),
            limit = NAME_FIELD_EXAMPLES,
        )
    if field.examples_policy == "distinct":
        ordered = sorted(counter, key = lambda value: stable_order_key(value = value))
        return ordered[:NAME_FIELD_EXAMPLES]
    return [value for value, _ in counter.most_common(OPEN_FIELD_EXAMPLES)]


def describe_field(*, field: FieldSpec, rows: list[dict[str, str]]) -> dict:
    """Собирает описание поля для словаря.

    Аргументы:
        field: описание поля.
        rows: строки сущности.

    Возвращает:
        Словарь с типом поля, наполнением и частотами.
    """
    counter = collect_field_values(field = field, rows = rows)
    described: dict = {
        "kind": field.kind,
        "filled_rows": sum(counter.values()),
        "distinct": len(counter),
    }
    if field.derived is not None:
        described["derived"] = field.derived
    if field.name in MULTIVALUE_FIELDS:
        described["multivalue"] = True

    if field.kind == "enum":
        described["values"] = [value for value, _ in counter.most_common()]
        described["frequencies"] = dict(counter.most_common())
    elif field.kind == "number":
        numbers = sorted({int(value) for value in counter if value.lstrip("-").isdigit()})
        described["minimum"] = numbers[0] if numbers else None
        described["maximum"] = numbers[-1] if numbers else None
        described["examples"] = [value for value, _ in counter.most_common(NUMBER_FIELD_EXAMPLES)]
    else:
        described["examples"] = pick_open_examples(field = field, rows = rows, counter = counter)
    return described



def project_row(*, entity: EntitySpec, row: dict[str, str]) -> dict:
    """Оставляет от строки таблицы только поля сущности.

    Аргументы:
        entity: описание сущности.
        row: исходная строка.

    Возвращает:
        Словарь «поле - значение»; мультизначное поле разворачивается в список,
        пустые значения опускаются.
    """
    projected: dict = {}
    for field in entity.fields:
        raw_value = row.get(column_of(field = field), "").strip()
        if not raw_value:
            continue
        if field.name in MULTIVALUE_FIELDS:
            parts = [part.strip() for part in raw_value.split(",") if part.strip()]
            if parts:
                projected[field.name] = parts
        else:
            projected[field.name] = to_code(field = field.name, value = raw_value)
    return projected


def askable_names_of(*, entity: EntitySpec, rows: list[dict[str, str]]) -> set[str]:
    """Возвращает имена, пригодные для вопроса о конкретном объекте.

    Аргументы:
        entity: описание сущности.
        rows: строки сущности.

    Возвращает:
        Множество имён; пустое, если у сущности нет поля имени.
    """
    name_field = next((field for field in entity.fields if field.name == "@name"), None)
    if name_field is None:
        return set()

    column = column_of(field = name_field)
    if not any("place_id" in row for row in rows[:1]):
        # У сущности отзывов имя не привязано к place_id: годится любое.
        return {
            row[column].strip()
            for row in rows
            if row.get(column, "").strip() and is_askable_name(name = row[column].strip())
        }

    places_by_name: dict[str, set[str]] = {}
    for row in rows:
        name = row.get(column, "").strip()
        place_id = row.get("place_id", "").strip()
        if name and place_id:
            places_by_name.setdefault(name, set()).add(place_id)
    return {
        name
        for name, place_ids in places_by_name.items()
        if len(place_ids) == 1 and is_askable_name(name = name)
    }


def sample_rows(*, entity: EntitySpec, rows: list[dict[str, str]]) -> list[dict]:
    """Отбирает образцы строк, покрывающие все значения перечислимых полей.

    Планировщик берёт значения условий из одной реальной строки - только так
    сочетание полей заведомо существует в данных. Чтобы у него был выбор под
    любое дефицитное значение, каждое значение перечня представлено несколькими
    строками.

    Аргументы:
        entity: описание сущности.
        rows: строки сущности.

    Возвращает:
        Образцы строк, спроецированные на поля сущности.
    """
    generator = random.Random(SAMPLE_SEED)
    shuffled = list(rows)
    generator.shuffle(shuffled)
    askable_names = askable_names_of(entity = entity, rows = rows)

    enum_fields = [field for field in entity.fields if field.kind == "enum"]
    per_value: dict[tuple[str, str], int] = {}
    picked: list[dict] = []
    seen: set[str] = set()

    def remember(row: dict[str, str]) -> None:
        projected = project_row(entity = entity, row = row)
        if "@name" in projected:
            projected["name_askable"] = projected["@name"] in askable_names
        signature = json.dumps(projected, ensure_ascii = False, sort_keys = True)
        if signature in seen:
            return
        seen.add(signature)
        picked.append(projected)
        for field in enum_fields:
            value = projected.get(field.name)
            values = value if isinstance(value, list) else [value]
            for item in values:
                if item is not None:
                    per_value[(field.name, item)] = per_value.get((field.name, item), 0) + 1

    # Сначала добираются редкие значения перечней, потом общий фон.
    for field in enum_fields:
        for row in shuffled:
            projected = project_row(entity = entity, row = row)
            value = projected.get(field.name)
            values = value if isinstance(value, list) else [value]
            for item in values:
                if item is None:
                    continue
                if per_value.get((field.name, item), 0) < ROWS_PER_ENUM_VALUE:
                    remember(row)
                    break

    for row in shuffled:
        if len(picked) >= MAXIMUM_SAMPLE_ROWS:
            break
        remember(row)

    return picked[:MAXIMUM_SAMPLE_ROWS]


def build_vocabulary(*, dataset_root: Path) -> dict:
    """Строит словарь значений по всем сущностям схемы.

    Аргументы:
        dataset_root: корень датасета КМВ.

    Возвращает:
        Словарь, пригодный для записи в json.
    """
    vocabulary: dict = {
        "dataset_root": str(dataset_root),
        "entities": {},
    }
    for entity in ENTITIES:
        rows = load_entity_rows(entity = entity, dataset_root = dataset_root)
        vocabulary["entities"][entity.name] = {
            "table": entity.table,
            "rows": len(rows),
            "fields": {
                field.name: describe_field(field = field, rows = rows)
                for field in entity.fields
            },
            "samples": sample_rows(entity = entity, rows = rows),
        }
    return vocabulary


def cli() -> None:
    """Точка входа командной строки."""
    parser = argparse.ArgumentParser(description = "выгрузка словаря значений ECQL")
    parser.add_argument("--dataset-root", required = True, type = Path, help = "корень датасета КМВ")
    parser.add_argument("--output", required = True, type = Path, help = "путь json со словарём")
    arguments = parser.parse_args()

    if not arguments.dataset_root.exists():
        raise SystemExit(f"нет каталога датасета: {arguments.dataset_root}")

    vocabulary = build_vocabulary(dataset_root = arguments.dataset_root)
    arguments.output.parent.mkdir(parents = True, exist_ok = True)
    arguments.output.write_text(
        json.dumps(vocabulary, ensure_ascii = False, indent = 2) + "\n",
        encoding = "utf-8",
    )

    for entity_name, entity in vocabulary["entities"].items():
        print(f"{entity_name}: строк {entity['rows']}, полей {len(entity['fields'])}")
    print(f"словарь записан: {arguments.output}")


if __name__ == "__main__":
    cli()
