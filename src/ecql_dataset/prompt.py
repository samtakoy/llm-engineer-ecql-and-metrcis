"""Промпты ECQL: что подаётся модели на обучении и на инференсе.

Два промпта отличаются только объёмом:

- короткий - роль и схема данных; им собирается поле `instruction` датасета и
  им же идут прогоны базовой модели и адаптера;
- полный - то же плюс правила языка словами; нужен прогону, который отвечает на
  вопрос «зачем адаптер, если грамматику можно описать в промпте».

Схема и списки полей собираются из словаря и `ecql.schema`, руками не пишутся:
после пополнения датасета промпт меняется сам.
"""

from ecql_dataset.ecql.grammar import (
    CONNECTIVES,
    OPERATORS,
    OUTPUT_FORMATS,
    OUTPUT_KEYWORD,
    START_KEYWORD,
    WHERE_KEYWORD,
)
from ecql_dataset.ecql.schema import (
    CONTAINMENT_OPERATORS,
    ENTITIES,
    MULTIVALUE_FIELDS,
    ORDER_OPERATORS,
    FieldSpec,
)

# Сколько примеров значений показывать у поля вне перечня.
FIELD_EXAMPLES = 4

# Окончание списка примеров. Отделяет открытое поле от перечня: перечень
# показан целиком, примеры - начало открытого списка.
EXAMPLES_TAIL = "и т.д."

# Роль и задача. Общая часть обоих промптов, стоит перед схемой.
INSTRUCTION_HEADER = (
    "Ты переводишь вопрос человека в запрос на ECQL - внутреннем языке запросов компании.\n"
    "Отвечай одной строкой запроса, без пояснений.\n"
    "\n"
    "Схема данных:"
)

# Заголовок раздела правил в полном промпте.
RULES_HEADER = "Правила языка:"

# Заголовок раздела запретов в полном промпте.
BANS_HEADER = "Запрещено:"

# Названия типов поля словами. Тип решает, какие операторы у поля допустимы и
# как пишется значение, поэтому стоит в схеме рядом с именем поля.
NUMBER_TYPE = "число"
STRING_TYPE = "строка"
MULTIVALUE_TYPE = "строка из значений через запятую"

# Смысл операторов словами. Часть словаря языка, а не данных. Порядок ключей -
# порядок перечисления в промпте: от простого сравнения к вхождению. В
# `grammar.OPERATORS` порядок другой, он задан разбором строки.
OPERATOR_MEANINGS: dict[str, str] = {
    "IS": "равно",
    "NOT": "не равно",
    "ABOVE": "больше",
    "BELOW": "меньше",
    "CONTAINS": "содержит значение",
    "NOT CONTAINS": "не содержит значение",
}

# Смысл связок словами.
CONNECTIVE_MEANINGS: dict[str, str] = {
    "&&": "и",
    "||": "или",
}

# Слова человека, по которым ставится суффикс вывода; из раздела 1 dz_ECQL.md.
SUFFIX_MARKERS: dict[str, tuple[str, ...]] = {
    "LIST": ("списком", "перечисли", "просто назови"),
    "TABLE": ("таблицей", "сравни", "в столбик"),
    "JSON": ("в json", "выгрузи", "для программы"),
}


def field_type(*, field: FieldSpec) -> str:
    """Называет тип поля словами.

    Аргументы:
        field: описание поля.

    Возвращает:
        Название типа для строки схемы.
    """
    if field.name in MULTIVALUE_FIELDS:
        return MULTIVALUE_TYPE
    if field.value_format == "bare":
        return NUMBER_TYPE
    return STRING_TYPE


def render_examples(*, examples: list[str]) -> str:
    """Собирает список примеров с окончанием открытого списка.

    Аргументы:
        examples: значения примеров.

    Возвращает:
        Строку вида «значение, значение и т.д.».
    """
    return ", ".join(examples) + " " + EXAMPLES_TAIL


def field_examples(*, entity_name: str, field: FieldSpec, vocabulary: dict) -> list[str]:
    """Собирает примеры значений поля.

    Примеры берутся из словаря, а у поля с `examples_hint` - из схемы: там
    выгрузка вводит в заблуждение, потому что все значения в данных однородны.

    Аргументы:
        entity_name: имя сущности поля.
        field: описание поля.
        vocabulary: словарь значений.

    Возвращает:
        Значения примеров.
    """
    if field.examples_hint is not None:
        return list(field.examples_hint)
    return vocabulary["entities"][entity_name]["fields"][field.name]["examples"][:FIELD_EXAMPLES]


def render_schema(*, vocabulary: dict) -> str:
    """Собирает схему данных: сущности, поля и их значения.

    Перечислимое поле показывается полным списком допустимых значений,
    остальные - примерами из словаря.

    Аргументы:
        vocabulary: словарь значений.

    Возвращает:
        Текст схемы.
    """
    lines: list[str] = []
    for entity in ENTITIES:
        described = vocabulary["entities"][entity.name]["fields"]
        lines.append("")
        lines.append(f"[{entity.name}]")
        for field in entity.fields:
            field_description = described[field.name]
            kind = field_type(field = field)
            if field_description["kind"] == "enum":
                values = ", ".join(field_description["values"])
                lines.append(f"- {field.name}, {kind}, допустимые значения: {values}")
            else:
                examples = field_examples(
                    entity_name = entity.name,
                    field = field,
                    vocabulary = vocabulary,
                )
                described_examples = render_examples(examples = examples)
                note = f"; {field.value_note}" if field.value_note else ""
                lines.append(f"- {field.name}, {kind}, примеры: {described_examples}{note}")
    return "\n".join(lines)


def render_rules() -> str:
    """Собирает правила языка словами: форма запроса, операторы, связки, вывод.

    Возвращает:
        Текст правил вместе с запретами.
    """
    if set(OPERATOR_MEANINGS) != set(OPERATORS):
        raise KeyError("список операторов промпта разошёлся с грамматикой")
    operators = ", ".join(
        f"{operator} {meaning}" for operator, meaning in OPERATOR_MEANINGS.items()
    )
    connectives = ", ".join(
        f"{connective} {CONNECTIVE_MEANINGS[connective]}" for connective in CONNECTIVES
    )
    formats = ", ".join(f"{OUTPUT_KEYWORD} {name}" for name in OUTPUT_FORMATS)

    rules = [
        RULES_HEADER,
        f"- запрос пишется одной строкой: {START_KEYWORD} [СУЩНОСТЬ] {WHERE_KEYWORD} условие"
        f" [связка условие] [{OUTPUT_KEYWORD} ФОРМАТ];",
        "- условие состоит из поля, оператора и значения: @city IS 'Кисловодск';",
        "- сущность пишется заглавными в квадратных скобках, поле - с префиксом @;",
        "- поле берётся из схемы своей сущности, чужие поля не подставляются;",
        f"- операторы: {operators};",
        f"- {' и '.join(ORDER_OPERATORS)} пишутся только у числовых полей;",
        f"- {' и '.join(CONTAINMENT_OPERATORS)} ищут подстроку и пишутся только у строковых полей;",
        f"- значение числового поля пишется без кавычек, строкового - в одинарных кавычках;",
        "- поле с допустимыми значениями принимает значение только из своего списка, дословно;",
        "- значение остальных полей берётся из вопроса и ставится в именительный падеж;",
        f"- условия соединяются связкой: {connectives};",
        f"- связка в запросе одна: {' и '.join(CONNECTIVES)} не смешиваются;",
        f"- суффикс вывода: {formats}; ставится, только когда человек назвал формат словами:",
    ]
    for name, markers in SUFFIX_MARKERS.items():
        rules.append(f"  {', '.join(markers)} - {OUTPUT_KEYWORD} {name};")
    rules.append("- про формат в вопросе не сказано - суффикс не пишется.")

    bans = [
        BANS_HEADER,
        "- писать SQL или любой другой язык запросов вместо ECQL;",
        "- придумывать сущности, поля и значения перечислимых полей, которых нет в схеме;",
        "- добавлять к запросу пояснения, обрамление кода и переносы строк;",
        "- заменять русское имя объекта или города переводом на латиницу.",
    ]
    return "\n".join(rules + [""] + bans)


def build_instruction(*, vocabulary: dict, with_rules: bool) -> str:
    """Собирает инструкцию модели.

    Инструкция одинакова во всех парах датасета и совпадает с той, что подаётся
    модели на инференсе: сравнение прогонов держится на посимвольном совпадении
    шаблона.

    Аргументы:
        vocabulary: словарь значений.
        with_rules: дописывать ли правила языка - отличие полного промпта от
            короткого.

    Возвращает:
        Текст инструкции.
    """
    instruction = INSTRUCTION_HEADER + "\n" + render_schema(vocabulary = vocabulary)
    if with_rules:
        instruction = instruction + "\n\n" + render_rules()
    return instruction


def build_messages(*, instruction: str, question: str) -> list[dict[str, str]]:
    """Собирает сообщения запроса к модели.

    Аргументы:
        instruction: текст инструкции.
        question: вопрос человека.

    Возвращает:
        Сообщения в формате чата: инструкция системой, вопрос пользователем.
    """
    return [
        {"role": "system", "content": instruction},
        {"role": "user", "content": question},
    ]


def build_training_messages(
    *,
    instruction: str,
    question: str,
    answer: str,
) -> list[dict[str, str]]:
    """Собирает сообщения обучающего примера.

    Аргументы:
        instruction: текст инструкции.
        question: вопрос человека.
        answer: эталонная строка ECQL.

    Возвращает:
        Сообщения запроса вместе с ответом ассистента.
    """
    return build_messages(instruction = instruction, question = question) + [
        {"role": "assistant", "content": answer},
    ]
