"""Схема ECQL: сущности и поля.

Для каждого поля: тип, колонка исходной таблицы, допустимые операторы, форма
записи значения. Плюс `ENUM_CODES` - как значение из csv записывается в ECQL.

Значения полей здесь не хранятся, они в vocabulary.json.
"""

from dataclasses import dataclass
from typing import Literal

FieldKind = Literal["enum", "open", "number"]
ExamplesPolicy = Literal["frequent", "distinct", "unique_by_category"]
Operator = Literal["IS", "NOT", "ABOVE", "BELOW", "CONTAINS", "NOT CONTAINS"]
ValueFormat = Literal["quoted", "bare"]

# Операторы по умолчанию: сравнение на равенство для перечней и строк.
EQUALITY_OPERATORS: tuple[str, ...] = ("IS", "NOT")

# Операторы для числовых полей.
ORDER_OPERATORS: tuple[str, ...] = ("ABOVE", "BELOW")

# Операторы вхождения: поиск подстроки. Допустимы у любого строкового поля.
CONTAINMENT_OPERATORS: tuple[str, ...] = ("CONTAINS", "NOT CONTAINS")

# Операторы строкового поля: сравнение целиком и поиск подстроки. Перечни сюда
# не входят - искать подстроку в коде значения нечего.
STRING_OPERATORS: tuple[str, ...] = EQUALITY_OPERATORS + CONTAINMENT_OPERATORS


@dataclass(frozen = True)
class FieldSpec:
    """Описание одного поля сущности.

    Аргументы:
        name: имя поля в ECQL вместе с префиксом.
        kind: enum - замкнутый перечень значений, open - открытая строка,
            number - число.
        column: колонка исходной таблицы; None у производных полей.
        derived: пояснение для производных полей; None у прямых.
        operators: операторы, допустимые для поля.
        value_format: как значение пишется в запросе - в кавычках или без.
        value_note: пометка к полю в промпте. Нужна особому значению, которое
            примерами не показать: по примерам городов не догадаться, что
            объект за чертой города записывается отдельным словом.
        examples_hint: примеры значений для промпта, написанные руками. Нужны
            там, где выгрузка из данных вводит в заблуждение: все города `@city`
            курортные, и модель принимает поле за перечень курортов, хотя поле
            открытое и город в нём любой.
        is_topic: называет ли поле предмет поиска. Числовой порог без такого
            поля вопросом не выражается: «что стоит от 1100 до 1300» - о чём?
        allows_enumeration: можно ли перечислять варианты поля через «или».
            Человек перечисляет типы объектов и города, но не имена и не оценки.
        examples_policy: как отбирать примеры значений. frequent - самые
            частые; distinct - выборка по разным значениям; unique_by_category -
            только имена, встречающиеся в таблице ровно раз, поровну по
            категориям.
    """

    name: str
    kind: FieldKind
    column: str | None
    derived: str | None
    operators: tuple[str, ...] = EQUALITY_OPERATORS
    value_format: ValueFormat = "quoted"
    examples_hint: tuple[str, ...] | None = None
    value_note: str | None = None
    allows_enumeration: bool = False
    is_topic: bool = False
    examples_policy: ExamplesPolicy = "frequent"


@dataclass(frozen = True)
class EntitySpec:
    """Описание сущности ECQL.

    Аргументы:
        name: имя сущности в ECQL без квадратных скобок.
        table: путь таблицы относительно корня датасета КМВ.
        fields: поля сущности.
    """

    name: str
    table: str
    fields: tuple[FieldSpec, ...]


PLACES = EntitySpec(
    name = "PLACES",
    table = "places/places.csv",
    fields = (
        FieldSpec(
            name = "@name",
            is_topic = True,
            kind = "open",
            column = "name",
            derived = None,
            operators = STRING_OPERATORS,
            examples_policy = "unique_by_category",
        ),
        FieldSpec(
            name = "@city",
            kind = "open",
            column = "city",
            derived = None,
            operators = STRING_OPERATORS,
            allows_enumeration = True,
            examples_hint = ("Москва", "Волгоград", "Пятигорск"),
            value_note = "объект вне населённого пункта - 'вне городов'",
        ),
        FieldSpec(
            name = "@category",
            is_topic = True,
            kind = "enum",
            column = "category",
            derived = None,
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@price_rub",
            kind = "number",
            column = "price_rub",
            derived = None,
            operators = ORDER_OPERATORS,
            value_format = "bare",
        ),
        FieldSpec(name = "@price_kind", kind = "enum", column = "price_kind", derived = None, is_topic = True),
        FieldSpec(name = "@object_kind", kind = "enum", column = "object_kind", derived = None, is_topic = True),
        FieldSpec(name = "@heritage_status", kind = "enum", column = "heritage_status", derived = None, is_topic = True),
        FieldSpec(name = "@wheelchair", kind = "enum", column = "wheelchair", derived = None),
    ),
)

REVIEWS = EntitySpec(
    name = "REVIEWS",
    table = "places/reviews.csv",
    fields = (
        FieldSpec(
            name = "@name",
            is_topic = True,
            kind = "open",
            column = "name",
            derived = None,
            operators = STRING_OPERATORS,
            examples_policy = "distinct",
        ),
        FieldSpec(
            name = "@city",
            kind = "open",
            column = "city",
            derived = None,
            operators = STRING_OPERATORS,
            allows_enumeration = True,
            examples_hint = ("Москва", "Волгоград", "Пятигорск"),
            value_note = "объект вне населённого пункта - 'вне городов'",
        ),
        FieldSpec(
            name = "@object_class",
            is_topic = True,
            kind = "enum",
            column = "object_class",
            derived = None,
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@rating",
            kind = "enum",
            column = "rating",
            derived = None,
            operators = EQUALITY_OPERATORS + ORDER_OPERATORS,
            value_format = "bare",
        ),
        FieldSpec(
            name = "@aspects",
            is_topic = True,
            kind = "enum",
            column = "aspects",
            derived = None,
            operators = STRING_OPERATORS,
        ),
    ),
)

PROXIMITY = EntitySpec(
    name = "PROXIMITY",
    table = "places/proximity.csv",
    fields = (
        FieldSpec(
            name = "@name",
            is_topic = True,
            kind = "open",
            column = None,
            derived = "имя объекта-якоря: places.name по place_id",
            operators = STRING_OPERATORS,
            examples_policy = "unique_by_category",
        ),
        FieldSpec(
            name = "@neighbour_category",
            is_topic = True,
            kind = "enum",
            column = "neighbour_category",
            derived = None,
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@distance_m",
            kind = "number",
            column = "distance_m",
            derived = None,
            operators = ORDER_OPERATORS,
            value_format = "bare",
        ),
    ),
)

FARES = EntitySpec(
    name = "FARES",
    table = "transit/leg_prices.csv",
    fields = (
        FieldSpec(
            name = "@transport",
            is_topic = True,
            kind = "enum",
            column = None,
            derived = "вид транспорта: routes.route_type по trips.trip_id",
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@route_start",
            is_topic = True,
            kind = "open",
            column = None,
            derived = "город отправления: routes.route_long_name по trips.trip_id",
            operators = STRING_OPERATORS,
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@route_end",
            is_topic = True,
            kind = "open",
            column = None,
            derived = "город прибытия: routes.route_long_name по trips.trip_id",
            operators = STRING_OPERATORS,
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@fare_class",
            is_topic = True,
            kind = "enum",
            column = "fare_class",
            derived = None,
            allows_enumeration = True,
        ),
        FieldSpec(
            name = "@price_rub",
            kind = "number",
            column = "price_rub",
            derived = None,
            operators = ORDER_OPERATORS,
            value_format = "bare",
        ),
    ),
)

ENTITIES = (PLACES, REVIEWS, PROXIMITY, FARES)

# Соответствие кода route_type из gtfs виду транспорта. Коды заданы стандартом
# gtfs, а не наполнением фида, поэтому список фиксирован.
ROUTE_TYPE_TO_TRANSPORT = {
    "0": "tram",
    "2": "suburban_train",
    "3": "bus",
    "102": "train",
    "200": "bus",
    "1100": "plane",
}

# Значения перечней в исходных таблицах записаны по-русски. Перечень в ECQL -
# часть словаря языка, а не данные, поэтому его значения переводятся в коды
# латиницей, как уже сделано у @category. Побочная выгода: русское значение
# модель списывает прямо из вопроса, и логическая точность меряет копирование
# подстроки вместо знания схемы; код такой шорткат убирает.
#
# Открытые поля - имена объектов, города, города маршрута - остаются как есть:
# это данные, а не словарь. Поле @aspects хранит перечисление из отзыва и тоже
# не переводится.
ENUM_CODES: dict[str, dict[str, str]] = {
    "@price_kind": {
        "средний чек": "average_check",
        "цена за ночь": "per_night",
    },
    "@object_kind": {
        "памятник": "monument",
        "ансамбль": "ensemble",
        "достопримечательное место": "heritage_site",
    },
    "@heritage_status": {
        "федеральный": "federal",
        "региональный": "regional",
        "местный": "local",
    },
    "@wheelchair": {
        "да": "yes",
        "нет": "no",
        "частично": "limited",
    },
    "@object_class": {
        "отель": "hotel",
        "гостевой дом": "guesthouse",
        "санаторий": "sanatorium",
        "хостел": "hostel",
    },
    "@transport": {
        "самолёт": "plane",
        "автобус": "bus",
        "поезд": "train",
        "трамвай": "tram",
        "электричка": "suburban_train",
    },
    "@fare_class": {
        "эконом": "economy",
        "бизнес": "business",
        "плацкарт": "platskart",
        "купе": "kupe",
    },
}


def to_code(*, field: str, value: str) -> str:
    """Переводит значение перечня из исходной таблицы в код ECQL.

    Аргументы:
        field: имя поля вместе с префиксом.
        value: значение из таблицы.

    Возвращает:
        Код латиницей; значение без перевода возвращается как есть.
    """
    return ENUM_CODES.get(field, {}).get(value, value)


# Поле @aspects хранит несколько значений через запятую.
MULTIVALUE_FIELDS = frozenset({"@aspects"})


def entity_by_name(*, name: str) -> EntitySpec:
    """Возвращает описание сущности по её имени.

    Аргументы:
        name: имя сущности без квадратных скобок.

    Возвращает:
        Описание сущности.
    """
    for entity in ENTITIES:
        if entity.name == name:
            return entity
    raise KeyError(f"неизвестная сущность: {name}")
