"""Проверка запроса ECQL по схеме и данным.

Проверки:
Сущность существует, поле принадлежит ей, оператор допустим для поля, значение
записано по типу поля и встречается в данных.
"""

from ecql_dataset.ecql.grammar import EcqlError, Query
from ecql_dataset.ecql.schema import MULTIVALUE_FIELDS, entity_by_name


def check_query(*, query: Query, vocabulary: dict) -> None:
    """Проверяет разобранный запрос по схеме и данным.

    Аргументы:
        query: разобранный запрос.
        vocabulary: словарь значений.
    """
    if query.entity not in vocabulary["entities"]:
        raise EcqlError(f"неизвестная сущность: [{query.entity}]")

    entity = entity_by_name(name = query.entity)
    specifications = {field.name: field for field in entity.fields}
    described = vocabulary["entities"][query.entity]["fields"]

    for condition in query.conditions:
        specification = specifications.get(condition.field)
        if specification is None:
            raise EcqlError(f"поле {condition.field} не принадлежит [{query.entity}]")
        if condition.operator not in specification.operators:
            raise EcqlError(
                f"оператор {condition.operator} недопустим для {condition.field}"
            )
        expected_quoted = specification.value_format == "quoted"
        if condition.quoted != expected_quoted:
            shape = "в кавычках" if expected_quoted else "без кавычек"
            raise EcqlError(f"значение {condition.field} записывается {shape}")

        field = described.get(condition.field, {})
        if field.get("kind") != "enum":
            continue
        values = field["values"]
        if condition.field in MULTIVALUE_FIELDS:
            # Поле хранит перечисление через запятую, фильтр идёт по подстроке.
            if not any(condition.value in value for value in values):
                raise EcqlError(f"значение {condition.value!r} не встречается в {condition.field}")
        elif condition.value not in values:
            raise EcqlError(f"значение {condition.value!r} не встречается в {condition.field}")
