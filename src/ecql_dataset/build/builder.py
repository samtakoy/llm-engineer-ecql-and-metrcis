"""Сборка датасета ECQL из рабочих md-листов.

Источник истины - md-листы: пара «вопрос человека - строка ECQL». Сборщик их
разбирает, проверяет каждую строку, раскладывает по сплитам и пишет jsonl в
формате домашнего задания плюс отчёт покрытия.

Пара, дописанная человеком сверх слотов планировщика, проходит наравне с
остальными: сборщик читает лист, а не slots.json.

Запуск:
    python -m ecql_dataset.build.builder \\
        --source dataset/ecql/source \\
        --output dataset/ecql \\
        --vocabulary dataset/ecql/source/vocabulary.json
        --glossary dataset/ecql/source/enum_glossary.json
"""

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from ecql_dataset.ecql.grammar import EcqlError, Query, parse
from ecql_dataset.ecql.schema import MULTIVALUE_FIELDS
from ecql_dataset.ecql.validate import check_query
from ecql_dataset.prompt import build_instruction

# Листы, которые читает сборщик; challenge читается отдельно и целиком уходит в тест.
SHEET_NAMES = ("places.md", "reviews.md", "proximity.md", "fares.md")
CHALLENGE_NAME = "challenge.md"

# Метка ненаписанного вопроса в листе.
QUESTION_PLACEHOLDER = "TODO"

# Доли сплитов. Тест отложен целиком, валидация отрезается от обучающей части.
TEST_SHARE = 0.20
VALIDATION_SHARE = 0.12

# Пороги покрытия из dz_ECQL_dataset.md, раздел 7.
FIELD_MINIMUM_TOTAL = 15
FIELD_MINIMUM_TEST = 2
VALUE_MINIMUM_TOTAL = 5
VALUE_MINIMUM_TEST = 1
OPERATOR_MINIMUM_TOTAL = 20
OPERATOR_MINIMUM_TEST = 3


@dataclass(frozen = True)
class Pair:
    """Пара датасета вместе с разобранным запросом.

    Аргументы:
        question: вопрос человека на русском.
        ecql: строка запроса.
        query: разобранный запрос.
        source: имя файла, откуда взята пара.
        challenge: пара из ручного набора, в обучение не идёт.
    """

    question: str
    ecql: str
    query: Query
    source: str
    challenge: bool

    @property
    def identifier(self) -> str:
        """Устойчивый ключ пары: первые двенадцать знаков хеша строки ECQL."""
        return hashlib.sha256(self.ecql.encode("utf-8")).hexdigest()[:12]

    @property
    def bucket(self) -> tuple[str, int]:
        """Корзина стратификации: сущность и число условий."""
        return (self.query.entity, len(self.query.conditions))


def read_sheet(*, path: Path, challenge: bool) -> list[tuple[str, str]]:
    """Читает пары из md-листа.

    Аргументы:
        path: путь листа.
        challenge: помечать ли пары как ручной набор.

    Возвращает:
        Список пар «вопрос - строка ECQL».
    """
    pairs: list[tuple[str, str]] = []
    pending: str | None = None
    for number, line in enumerate(path.read_text(encoding = "utf-8").split("\n"), start = 1):
        stripped = line.strip()
        if stripped.startswith("- "):
            pending = stripped[2:].strip()
        elif stripped.startswith("→ "):
            if pending is None:
                raise EcqlError(f"{path.name}:{number}: запрос без вопроса")
            if pending == QUESTION_PLACEHOLDER:
                raise EcqlError(f"{path.name}:{number}: вопрос не написан")
            pairs.append((pending, stripped[2:].strip()))
            pending = None
        elif not stripped:
            pending = None
    return pairs


def collect_pairs(*, directory: Path, vocabulary: dict) -> list[Pair]:
    """Читает и проверяет все листы каталога.

    Аргументы:
        directory: каталог с листами.
        vocabulary: словарь значений.

    Возвращает:
        Список проверенных пар.
    """
    pairs: list[Pair] = []
    seen: dict[str, str] = {}
    sources = [(name, False) for name in SHEET_NAMES] + [(CHALLENGE_NAME, True)]

    for name, challenge in sources:
        path = directory / name
        if not path.exists():
            if challenge:
                continue
            raise EcqlError(f"нет листа {name}")
        for question, ecql in read_sheet(path = path, challenge = challenge):
            try:
                query = parse(query = ecql)
                check_query(query = query, vocabulary = vocabulary)
            except EcqlError as error:
                raise EcqlError(f"{name}: {error}\n  {ecql}") from error
            if ecql in seen:
                raise EcqlError(f"{name}: запрос повторяет пару из {seen[ecql]}\n  {ecql}")
            seen[ecql] = name
            pairs.append(Pair(
                question = question,
                ecql = ecql,
                query = query,
                source = name,
                challenge = challenge,
            ))
    return pairs


def split_pairs(*, pairs: list[Pair]) -> dict[str, list[Pair]]:
    """Раскладывает пары на train, val и test.

    Раскладка стратифицирована по корзине сущность × число условий и
    воспроизводима: порядок внутри корзины задаёт хеш строки ECQL, а не порядок
    строк в файле. Ручной набор целиком уходит в тест.

    Аргументы:
        pairs: проверенные пары.

    Возвращает:
        Соответствие «имя сплита - пары».
    """
    splits: dict[str, list[Pair]] = {"train": [], "val": [], "test": []}

    buckets: dict[tuple[str, int], list[Pair]] = {}
    for pair in pairs:
        if pair.challenge:
            splits["test"].append(pair)
            continue
        buckets.setdefault(pair.bucket, []).append(pair)

    for bucket in sorted(buckets):
        ordered = sorted(buckets[bucket], key = lambda item: item.identifier)
        size = len(ordered)
        test_size = round(size * TEST_SHARE)
        validation_size = round(size * VALIDATION_SHARE)
        splits["test"].extend(ordered[:test_size])
        splits["val"].extend(ordered[test_size:test_size + validation_size])
        splits["train"].extend(ordered[test_size + validation_size:])

    return splits


def build_record(*, pair: Pair, instruction: str) -> dict:
    """Собирает строку датасета.

    Аргументы:
        pair: пара датасета.
        instruction: общая инструкция.

    Возвращает:
        Словарь для записи в jsonl.
    """
    fields: list[str] = []
    operators: list[str] = []
    for condition in pair.query.conditions:
        if condition.field not in fields:
            fields.append(condition.field)
        if condition.operator not in operators:
            operators.append(condition.operator)

    numeric_fields = [
        condition.field for condition in pair.query.conditions
        if condition.operator in ("ABOVE", "BELOW")
    ]
    return {
        "instruction": instruction,
        "input": pair.question,
        "output": pair.ecql,
        "meta": {
            "id": pair.identifier,
            "entity": pair.query.entity,
            "conditions": len(pair.query.conditions),
            "connective": pair.query.connective,
            "fields": fields,
            "operators": operators,
            "suffix": pair.query.suffix,
            "has_range": len(numeric_fields) != len(set(numeric_fields)),
            "source": pair.source,
            "challenge": pair.challenge,
        },
    }


def write_jsonl(*, path: Path, records: list[dict]) -> None:
    """Записывает строки датасета в jsonl.

    Аргументы:
        path: путь файла.
        records: строки датасета.
    """
    with path.open("w", encoding = "utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii = False) + "\n")


def count_axis(*, splits: dict[str, list[Pair]], key) -> dict[str, dict[str, int]]:
    """Считает вхождения значений оси по сплитам.

    Аргументы:
        splits: пары по сплитам.
        key: функция, возвращающая список значений оси для пары.

    Возвращает:
        Соответствие «значение оси - счётчики по сплитам и всего».
    """
    counts: dict[str, dict[str, int]] = {}
    for split, pairs in splits.items():
        for pair in pairs:
            for value in key(pair):
                row = counts.setdefault(str(value), {"train": 0, "val": 0, "test": 0, "всего": 0})
                row[split] += 1
                row["всего"] += 1
    return counts


def render_table(*, title: str, counts: dict[str, dict[str, int]]) -> list[str]:
    """Собирает таблицу отчёта по одной оси.

    Аргументы:
        title: заголовок таблицы.
        counts: счётчики оси.

    Возвращает:
        Строки отчёта.
    """
    lines = [f"## {title}", "", "| Значение | train | val | test | всего |", "|---|---|---|---|---|"]
    for value in sorted(counts, key = lambda item: (-counts[item]["всего"], item)):
        row = counts[value]
        lines.append(f"| {value} | {row['train']} | {row['val']} | {row['test']} | {row['всего']} |")
    lines.append("")
    return lines


def enum_values_of(*, pair: Pair, vocabulary: dict) -> set[str]:
    """Возвращает значения перечней, которые задействует пара.

    Фильтр по мультизначному полю идёт подстрокой: `CONTAINS 'бассейн'`
    отбирает строки со значением `бассейн и спа`. Подстрока значением поля не
    является, поэтому засчитывается в те значения словаря, в которые попадает,
    а не в отдельную строку отчёта.

    Аргументы:
        pair: пара датасета.
        vocabulary: словарь значений.

    Возвращает:
        Множество ключей вида «сущность.поле = значение».
    """
    described = vocabulary["entities"][pair.query.entity]["fields"]
    used: set[str] = set()
    for condition in pair.query.conditions:
        field = described[condition.field]
        if field["kind"] != "enum":
            continue
        if condition.field in MULTIVALUE_FIELDS:
            matched = [value for value in field["values"] if condition.value in value]
        else:
            matched = [condition.value]
        for value in matched:
            used.add(f"{pair.query.entity}.{condition.field} = {value}")
    return used


def find_violations(*, splits: dict[str, list[Pair]], vocabulary: dict) -> list[str]:
    """Ищет нарушения порогов покрытия.

    Аргументы:
        splits: пары по сплитам.
        vocabulary: словарь значений.

    Возвращает:
        Список описаний нарушений.
    """
    violations: list[str] = []

    fields = count_axis(
        splits = splits,
        key = lambda pair: {condition.field for condition in pair.query.conditions},
    )
    for name, row in sorted(fields.items()):
        if row["всего"] < FIELD_MINIMUM_TOTAL:
            violations.append(f"поле {name}: {row['всего']} из {FIELD_MINIMUM_TOTAL} всего")
        if row["test"] < FIELD_MINIMUM_TEST:
            violations.append(f"поле {name}: {row['test']} из {FIELD_MINIMUM_TEST} в тесте")

    operators = count_axis(
        splits = splits,
        key = lambda pair: {condition.operator for condition in pair.query.conditions},
    )
    for name, row in sorted(operators.items()):
        if row["всего"] < OPERATOR_MINIMUM_TOTAL:
            violations.append(f"оператор {name}: {row['всего']} из {OPERATOR_MINIMUM_TOTAL} всего")
        if row["test"] < OPERATOR_MINIMUM_TEST:
            violations.append(f"оператор {name}: {row['test']} из {OPERATOR_MINIMUM_TEST} в тесте")

    values = count_axis(
        splits = splits,
        key = lambda pair: enum_values_of(pair = pair, vocabulary = vocabulary),
    )
    for name, row in sorted(values.items()):
        if row["всего"] < VALUE_MINIMUM_TOTAL:
            violations.append(f"значение {name}: {row['всего']} из {VALUE_MINIMUM_TOTAL} всего")
        if row["test"] < VALUE_MINIMUM_TEST:
            violations.append(f"значение {name}: {row['test']} из {VALUE_MINIMUM_TEST} в тесте")

    return violations


def render_coverage(*, splits: dict[str, list[Pair]], vocabulary: dict) -> str:
    """Собирает отчёт покрытия.

    Аргументы:
        splits: пары по сплитам.
        vocabulary: словарь значений.

    Возвращает:
        Текст отчёта.
    """
    lines = [
        "# Покрытие датасета ECQL",
        "",
        "Отчёт собирается `ecql_dataset.builder`; руками не правится.",
        "",
        "| Сплит | Строк |",
        "|---|---|",
    ]
    for split in ("train", "val", "test"):
        lines.append(f"| {split} | {len(splits[split])} |")
    challenge = sum(1 for pair in splits["test"] if pair.challenge)
    lines.append(f"| в том числе challenge | {challenge} |")
    lines.append("")

    lines += render_table(
        title = "Сущность",
        counts = count_axis(splits = splits, key = lambda pair: [pair.query.entity]),
    )
    lines += render_table(
        title = "Число условий",
        counts = count_axis(splits = splits, key = lambda pair: [len(pair.query.conditions)]),
    )
    lines += render_table(
        title = "Связка",
        counts = count_axis(
            splits = splits,
            key = lambda pair: [pair.query.connective or "нет"],
        ),
    )
    lines += render_table(
        title = "Суффикс вывода",
        counts = count_axis(splits = splits, key = lambda pair: [pair.query.suffix or "нет"]),
    )
    lines += render_table(
        title = "Оператор",
        counts = count_axis(
            splits = splits,
            key = lambda pair: {condition.operator for condition in pair.query.conditions},
        ),
    )
    lines += render_table(
        title = "Поле",
        counts = count_axis(
            splits = splits,
            key = lambda pair: {
                f"{pair.query.entity}.{condition.field}" for condition in pair.query.conditions
            },
        ),
    )

    violations = find_violations(splits = splits, vocabulary = vocabulary)
    lines.append("## Нарушенные пороги")
    lines.append("")
    if violations:
        lines += [f"- {violation}" for violation in violations]
    else:
        lines.append("Нет.")
    lines.append("")
    return "\n".join(lines)


def cli() -> None:
    """Точка входа командной строки."""
    parser = argparse.ArgumentParser(description = "сборка датасета ECQL из md-листов")
    parser.add_argument("--source", required = True, type = Path, help = "каталог листов")
    parser.add_argument("--output", required = True, type = Path, help = "каталог датасета")
    parser.add_argument("--vocabulary", required = True, type = Path, help = "словарь значений")
    parser.add_argument("--glossary", required = True, type = Path, help = "расшифровки значений")
    arguments = parser.parse_args()

    vocabulary = json.loads(arguments.vocabulary.read_text(encoding = "utf-8"))
    glossary = json.loads(arguments.glossary.read_text(encoding = "utf-8"))
    pairs = collect_pairs(directory = arguments.source, vocabulary = vocabulary)
    splits = split_pairs(pairs = pairs)
    instruction = build_instruction(
        vocabulary = vocabulary,
        glossary = glossary,
        with_rules = False,
    )

    arguments.output.mkdir(parents = True, exist_ok = True)
    for split, split_pairs_list in splits.items():
        ordered = sorted(split_pairs_list, key = lambda item: item.identifier)
        records = [build_record(pair = pair, instruction = instruction) for pair in ordered]
        path = arguments.output / f"{split}.jsonl"
        write_jsonl(path = path, records = records)
        print(f"{path}: строк {len(records)}")

    coverage_path = arguments.output / "coverage.md"
    coverage_path.write_text(
        render_coverage(splits = splits, vocabulary = vocabulary),
        encoding = "utf-8",
    )
    violations = find_violations(splits = splits, vocabulary = vocabulary)
    print(f"{coverage_path}: нарушенных порогов {len(violations)}")


if __name__ == "__main__":
    cli()
