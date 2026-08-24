"""Грамматика ECQL: разбор строки запроса на части и сборка обратно.

Модуль ничего не знает о датасете. Он отвечает на один вопрос: разбирается ли
строка по правилам языка и что в ней написано. Проверка того, что поле
принадлежит сущности, а значение есть в данных, живёт в `builder`.

Разбор нужен дважды: при сборке датасета - на эталонах, и при оценке - на
ответах модели, где строка может быть какой угодно. Поэтому ошибки разбора
описаны текстом и не гасятся.
"""

import re
from dataclasses import dataclass

# Слова языка.
START_KEYWORD = "FETCH"
WHERE_KEYWORD = "WHERE"
OUTPUT_KEYWORD = "AS"

# Допустимые форматы вывода.
OUTPUT_FORMATS = ("JSON", "TABLE", "LIST")

# Операторы; составной проверяется раньше простого, иначе `NOT CONTAINS`
# разберётся как `NOT` со значением `CONTAINS`.
OPERATORS = ("NOT CONTAINS", "CONTAINS", "ABOVE", "BELOW", "IS", "NOT")

# Связки условий.
CONNECTIVES = ("&&", "||")

QUERY_PATTERN = re.compile(
    rf"^{START_KEYWORD}\s+\[([A-Z_]+)\]\s+{WHERE_KEYWORD}\s+(.+?)"
    rf"(?:\s+{OUTPUT_KEYWORD}\s+([A-Z]+))?$"
)
CONDITION_PATTERN = re.compile(
    r"^(@[a-z_]+)\s+(" + "|".join(OPERATORS) + r")\s+(?:'([^']*)'|(-?\d+))$"
)


class EcqlError(ValueError):
    """Строка не разбирается по грамматике ECQL."""


@dataclass(frozen = True)
class Condition:
    """Одно условие запроса.

    Аргументы:
        field: имя поля вместе с префиксом.
        operator: оператор сравнения или вхождения.
        value: значение как текст; число хранится тоже текстом.
        quoted: было ли значение записано в кавычках.
    """

    field: str
    operator: str
    value: str
    quoted: bool


@dataclass(frozen = True)
class Query:
    """Разобранный запрос.

    Аргументы:
        entity: имя сущности без квадратных скобок.
        conditions: условия в порядке записи.
        connective: связка между условиями; None при одном условии.
        suffix: формат вывода без ключевого слова; None, если не указан.
    """

    entity: str
    conditions: tuple[Condition, ...]
    connective: str | None
    suffix: str | None


def split_conditions(*, text: str) -> tuple[list[str], str | None]:
    """Разрезает часть после WHERE на условия по связке.

    Связки не смешиваются: приоритет операций спецификацией не задан, поэтому
    запрос с `&&` и `||` разом читается двояко и считается ошибкой.

    Аргументы:
        text: часть запроса после WHERE.

    Возвращает:
        Список кусков и связку; связка None при единственном условии.
    """
    used = [connective for connective in CONNECTIVES if f" {connective} " in f" {text} "]
    if len(used) > 1:
        raise EcqlError("связки && и || смешаны в одном запросе")
    if not used:
        return [text.strip()], None

    connective = used[0]
    parts = [part.strip() for part in text.split(connective)]
    if any(not part for part in parts):
        raise EcqlError(f"пустое условие рядом со связкой {connective}")
    return parts, connective


def parse_condition(*, text: str) -> Condition:
    """Разбирает одно условие.

    Аргументы:
        text: текст условия.

    Возвращает:
        Условие.
    """
    match = CONDITION_PATTERN.match(text)
    if match is None:
        raise EcqlError(f"условие не разбирается: {text!r}")
    field, operator, quoted_value, bare_value = match.groups()
    return Condition(
        field = field,
        operator = operator,
        value = quoted_value if quoted_value is not None else bare_value,
        quoted = quoted_value is not None,
    )


def parse(*, query: str) -> Query:
    """Разбирает строку запроса.

    Аргументы:
        query: строка ECQL.

    Возвращает:
        Разобранный запрос.
    """
    text = query.strip()
    if not text:
        raise EcqlError("пустая строка")

    match = QUERY_PATTERN.match(text)
    if match is None:
        raise EcqlError(f"запрос не разбирается по грамматике: {text!r}")

    entity, body, suffix = match.groups()
    if suffix is not None and suffix not in OUTPUT_FORMATS:
        raise EcqlError(f"неизвестный формат вывода: {suffix}")

    parts, connective = split_conditions(text = body)
    conditions = tuple(parse_condition(text = part) for part in parts)
    return Query(entity = entity, conditions = conditions, connective = connective, suffix = suffix)


def canonical(*, query: Query) -> tuple:
    """Приводит запрос к виду, не зависящему от порядка условий.

    Перестановка условий смысла запроса не меняет, поэтому сравнение ответа
    модели с эталоном идёт по этому виду, а не по строке.

    Аргументы:
        query: разобранный запрос.

    Возвращает:
        Кортеж, пригодный для сравнения и хеширования.
    """
    conditions = tuple(sorted(
        (condition.field, condition.operator, condition.value)
        for condition in query.conditions
    ))
    return (query.entity, conditions, query.connective, query.suffix)


def render(*, query: Query) -> str:
    """Собирает строку запроса обратно из разобранных частей.

    Аргументы:
        query: разобранный запрос.

    Возвращает:
        Строку ECQL.
    """
    parts = []
    for condition in query.conditions:
        value = f"'{condition.value}'" if condition.quoted else condition.value
        parts.append(f"{condition.field} {condition.operator} {value}")
    connective = f" {query.connective} " if query.connective else " "
    body = connective.join(parts)
    suffix = f" {OUTPUT_KEYWORD} {query.suffix}" if query.suffix else ""
    return f"{START_KEYWORD} [{query.entity}] {WHERE_KEYWORD} {body}{suffix}"
