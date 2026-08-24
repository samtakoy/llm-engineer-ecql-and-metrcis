"""Генерация и чтение рабочих md-листов датасета ECQL.

Лист - это то, что правит человек: вопрос на русском и готовая строка ECQL под
ним. Строка разметки после ответа выводится из самого запроса и показывает,
какие оси закрывает пара; правится она только через перегенерацию.

Повторный запуск не затирает написанные вопросы: они переносятся в новый лист
по строке ECQL.

Запуск:
    python -m ecql_dataset.build.sheets \\
        --slots dataset/ecql/source/slots.json \\
        --directory dataset/ecql/source
"""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from ecql_dataset.ecql.schema import ENTITIES, entity_by_name

# Метка вопроса, который ещё не написан.
QUESTION_PLACEHOLDER = "TODO"

# Заголовки разделов по числу условий в запросе.
CONDITION_HEADINGS = {
    1: "Одно условие",
    2: "Два условия",
    3: "Три условия",
    4: "Четыре условия",
}


@dataclass
class Pair:
    """Пара датасета: вопрос человека и запрос на ECQL.

    Аргументы:
        question: формулировка на русском.
        ecql: строка запроса.
    """

    question: str
    ecql: str


def describe_axes(*, slot: dict) -> str:
    """Составляет строку разметки со сводкой осей слота.

    Аргументы:
        slot: слот планировщика.

    Возвращает:
        Строку без ведущего символа комментария.
    """
    entity = entity_by_name(name = slot["entity"])
    field_by_name = {field.name: field for field in entity.fields}

    fields: list[str] = []
    operators: list[str] = []
    for condition in slot["conditions"]:
        if condition["field"] not in fields:
            fields.append(condition["field"])
        if condition["operator"] not in operators:
            operators.append(condition["operator"])

    parts = [
        f"слот {slot['index']}",
        f"{len(slot['conditions'])} условия" if len(slot["conditions"]) != 1 else "одно условие",
        slot["connective"] or "без связки",
        slot["suffix"] or "без суффикса",
    ]
    if slot["has_range"]:
        parts.append("диапазон")
    if any(field_by_name[name].is_topic for name in fields):
        parts.append("предмет назван")
    parts.append("поля " + " ".join(fields))
    parts.append("операторы " + " ".join(operators))
    return " · ".join(parts)


def read_sheet(*, sheet_path: Path) -> dict[str, str]:
    """Читает написанные вопросы из существующего листа.

    Аргументы:
        sheet_path: путь листа.

    Возвращает:
        Соответствие «строка ECQL - вопрос»; пустое, если листа нет.
    """
    if not sheet_path.exists():
        return {}

    questions: dict[str, str] = {}
    pending: list[str] = []
    for line in sheet_path.read_text(encoding = "utf-8").split("\n"):
        stripped = line.strip()
        if stripped.startswith("- "):
            pending.append(stripped[2:].strip())
        elif stripped.startswith("→ "):
            if pending:
                questions[stripped[2:].strip()] = pending[-1]
            pending = []
        elif not stripped:
            pending = []
    return questions


def render_sheet(*, entity_name: str, slots: list[dict], questions: dict[str, str]) -> str:
    """Собирает текст листа по слотам сущности.

    Аргументы:
        entity_name: имя сущности.
        slots: слоты этой сущности.
        questions: ранее написанные вопросы по строке ECQL.

    Возвращает:
        Текст md-листа.
    """
    lines = [
        f"# {entity_name}",
        "",
        "Вопрос пишется человеком, строка ECQL и строка разметки после неё -",
        "результат генерации. Перезапуск генератора вопросы сохраняет.",
        "",
    ]

    by_count: dict[int, list[dict]] = {}
    for slot in slots:
        by_count.setdefault(len(slot["conditions"]), []).append(slot)

    for count in sorted(by_count):
        lines.append(f"## {CONDITION_HEADINGS.get(count, f'{count} условий')}")
        lines.append("")
        for slot in sorted(by_count[count], key = lambda item: item["index"]):
            question = questions.get(slot["ecql"], QUESTION_PLACEHOLDER)
            lines.append(f"- {question}")
            lines.append(f"  → {slot['ecql']}")
            lines.append(f"  # {describe_axes(slot = slot)}")
            lines.append("")

    return "\n".join(lines)


def cli() -> None:
    """Точка входа командной строки."""
    parser = argparse.ArgumentParser(description = "генерация рабочих листов датасета ECQL")
    parser.add_argument("--slots", required = True, type = Path, help = "слоты планировщика")
    parser.add_argument("--directory", required = True, type = Path, help = "каталог листов")
    arguments = parser.parse_args()

    slots = json.loads(arguments.slots.read_text(encoding = "utf-8"))
    arguments.directory.mkdir(parents = True, exist_ok = True)

    for entity in ENTITIES:
        entity_slots = [slot for slot in slots if slot["entity"] == entity.name]
        sheet_path = arguments.directory / f"{entity.name.lower()}.md"
        questions = read_sheet(sheet_path = sheet_path)
        sheet_path.write_text(
            render_sheet(entity_name = entity.name, slots = entity_slots, questions = questions),
            encoding = "utf-8",
        )
        written = sum(
            1 for slot in entity_slots
            if questions.get(slot["ecql"], QUESTION_PLACEHOLDER) != QUESTION_PLACEHOLDER
        )
        print(f"{sheet_path}: пар {len(entity_slots)}, вопросов написано {written}")


if __name__ == "__main__":
    cli()
