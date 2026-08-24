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
    parse,
)
from ecql_dataset.ecql.schema import (
    CONTAINMENT_OPERATORS,
    ENTITIES,
    EQUALITY_OPERATORS,
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
RULES_HEADER = "Правила языка ECQL:"

# Образцы перевода. Описание формы словами модель удерживает хуже, чем готовую
# пару «вопрос - ответ»: без образца базовая модель пишет условия без каркаса
# запроса. Пар несколько и значения в них разные, иначе модель переносит числа и
# имена из единственного примера прямо в ответ.
#
# Пары написаны руками и ни из одной выборки не взяты: промпт не должен зависеть
# от содержимого датасета. Каждая проверяется грамматикой и схемой при сборке
# правил, поэтому разойтись с языком молча не может.
EXAMPLE_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "Что пишут про завтраки в гостевых домах?",
        "FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' && @object_class IS 'guesthouse'",
    ),
    (
        "Ессентуки и Пятигорск, давай списком",
        "FETCH [PLACES] WHERE @city IS 'Ессентуки' || @city IS 'Пятигорск' AS LIST",
    ),
    (
        "Поезда до Ростова-на-Дону стоимостью от тысячи до трёх, покажи в формате json",
        "FETCH [FARES] WHERE @transport IS 'train' && @price_rub ABOVE 1000"
        " && @price_rub BELOW 3000 AS JSON",
    ),
)

# Заголовок блока примеров и подписи пары.
EXAMPLES_HEADER = "Примеры перевода вопроса в запрос:"
EXAMPLE_QUESTION_LABEL = "Вопрос от пользователя:"
EXAMPLE_ANSWER_LABEL = "Ответ:"

# Оговорка после примеров: без неё модель переносит из них значения.
EXAMPLES_NOTE = (
    "Примеры показывают форму запроса. Значения из них в ответ не переносятся:"
    " сущность, поля и значения берутся из вопроса пользователя."
)

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

# Слово, которым пользователь называет формат вывода. Начальная форма, без
# падежей: склонять за модель не нужно. Глаголы рядом - «покажи», «дай»,
# «сведи» - формат не задают и в список не идут.
SUFFIX_MARKERS: dict[str, str] = {
    "LIST": "список",
    "TABLE": "таблица",
    "JSON": "json",
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
    """Собирает правила языка словами.

    Правила разложены по блокам - форма запроса, поля и значения, операторы,
    связки, формат вывода, формат ответа, запреты. Один блок отвечает на один
    вопрос: описание сплошным списком модель держит хуже.

    Возвращает:
        Текст правил.
    """
    if set(OPERATOR_MEANINGS) != set(OPERATORS):
        raise KeyError("список операторов промпта разошёлся с грамматикой")
    for _, answer in EXAMPLE_PAIRS:
        parse(query = answer)

    equality = ", ".join(
        f"{operator} {OPERATOR_MEANINGS[operator]}" for operator in EQUALITY_OPERATORS
    )
    order = ", ".join(
        f"{operator} {OPERATOR_MEANINGS[operator]}" for operator in ORDER_OPERATORS
    )
    containment = ", ".join(
        f"{operator} {OPERATOR_MEANINGS[operator]}" for operator in CONTAINMENT_OPERATORS
    )
    connectives = ", ".join(
        f"{connective} это {CONNECTIVE_MEANINGS[connective]}" for connective in CONNECTIVES
    )
    formats = ", ".join(f"{OUTPUT_KEYWORD} {name}" for name in OUTPUT_FORMATS)
    markers = "; ".join(
        f"{word} - {OUTPUT_KEYWORD} {name}"
        for name, word in SUFFIX_MARKERS.items()
    )

    example_lines: list[str] = []
    for question, answer in EXAMPLE_PAIRS:
        example_lines.append(f"{EXAMPLE_QUESTION_LABEL} {question}")
        example_lines.append(f"{EXAMPLE_ANSWER_LABEL} {answer}")
        example_lines.append("")

    lines = [
        RULES_HEADER,
        "",
        "Формат запроса:",
        f"- запрос начинается словом {START_KEYWORD};",
        "- дальше сущность заглавными в квадратных скобках, пример: [PLACES];",
        f"- дальше слово {WHERE_KEYWORD} и условия;",
        "- в конце может стоять формат вывода, но только если пользователь его ЯВНО"
        f" попросил, пример: {OUTPUT_KEYWORD} LIST; иначе формат вывода опускается;",
        "",
        "Поля и значения:",
        "- поле пишется с префиксом @, пример: @city;",
        "- строка пишется в кавычках, пример: 'Кисловодск';",
        "- число пишется без кавычек, пример: 700;",
        "",
        "Операторы:",
        f"- {equality} - допустимы у полей любого типа;",
        f"- {order} - только у числовых полей;",
        f"- {containment} - только у строковых полей;",
        "",
        "Логические связки для условий:",
        f"- {connectives};",
        "- в одном запросе допустимы связки только одного типа:"
        f" {' и '.join(CONNECTIVES)} одновременно использовать нельзя;",
        "",
        "Формат вывода:",
        f"- {formats};",
        f"- ставится, только когда пользователь явно указал требуемый формат: {markers};",
        "- формат в вопросе не указан - не пишется.",
        "",
        "Формат ответа:",
        "- только итоговый запрос на языке ECQL, в который преобразован вопрос пользователя.",
        "",
        EXAMPLES_HEADER,
        "",
        *example_lines,
        EXAMPLES_NOTE,
        "",
        BANS_HEADER,
        "- использовать поля и значения, которых нет в схеме;",
        "- добавлять пояснения и обрамление кода.",
    ]
    return "\n".join(lines)


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
