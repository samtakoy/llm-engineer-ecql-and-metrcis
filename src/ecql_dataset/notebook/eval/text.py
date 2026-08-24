"""Референсные текстовые метрики: насколько ответ похож на эталон как текст.

Метрики:
- exact - посимвольное совпадение;
- token_f1 - пересечение мешков токенов;
- bleu, nist - точность по n-граммам, из nltk;
- meteor - совпадение с учётом порядка, из nltk;
- rouge_l - самая длинная общая подпоследовательность;
- cider - взвешенные по редкости n-граммы.

Испорченное значение почти не роняет их, а смысл запроса
меняет полностью. Считаются рядом с продуктовыми, чтобы это показать.

Токенизация - по элементам ECQL: слова, числа и знаки языка (Скобки, @, кавычки и & становятся отдельными токенами).

Зачем:
 BLEU и ROUGE считают по токенам.
 Если резать по пробелам, 'food' — один токен вместе с кавычками, а [PLACES] — вместе со скобками.
 Тогда пропущенная скобка или потерянная кавычка вообще не видна метрике:
  токен просто другой, как если бы поменяли слово.
 Разбив знаки отдельно, метрика различает «модель написала другое значение» и «модель забыла скобку».
"""

import re
from collections import Counter

from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from nltk.translate.nist_score import sentence_nist

# Токен ECQL: слово с подчёркиванием и дефисом, число или знак языка.
TOKEN_PATTERN = re.compile(r"[^\W\d_][\w-]*|\d+|[\[\]@&|']")

# Длина n-грамм для cider.
CIDER_ORDERS = (1, 2, 3, 4)

SMOOTHING = SmoothingFunction().method1


class NoWordNet:
    """Заглушка вместо WordNet: meteor не лезет в сеть и повторяем от прогона к прогону."""

    def synsets(self, word: str) -> list:
        """Возвращает пустой список синонимов.

        Аргументы:
            word: слово.

        Возвращает:
            Пустой список.
        """
        return []


NO_WORDNET = NoWordNet()


def tokens_of(*, text: str) -> list[str]:
    """Режет строку на токены.

    Аргументы:
        text: строка ECQL или ответ модели.

    Возвращает:
        Список токенов в нижнем регистре.
    """
    return TOKEN_PATTERN.findall(text.lower())


def token_f1(*, prediction: str, reference: str) -> float:
    """Считает F1 по мешкам токенов.

    Аргументы:
        prediction: ответ модели.
        reference: эталон.

    Возвращает:
        Значение от нуля до единицы.
    """
    predicted = Counter(tokens_of(text = prediction))
    expected = Counter(tokens_of(text = reference))
    overlap = sum((predicted & expected).values())
    if not overlap:
        return 0.0
    precision = overlap / sum(predicted.values())
    recall = overlap / sum(expected.values())
    return 2 * precision * recall / (precision + recall)


def rouge_l(*, prediction: str, reference: str) -> float:
    """Считает ROUGE-L: F1 по длине наибольшей общей подпоследовательности.

    Аргументы:
        prediction: ответ модели.
        reference: эталон.

    Возвращает:
        Значение от нуля до единицы.
    """
    predicted = tokens_of(text = prediction)
    expected = tokens_of(text = reference)
    if not predicted or not expected:
        return 0.0

    row = [0] * (len(predicted) + 1)
    for expected_token in expected:
        previous = 0
        for index, predicted_token in enumerate(predicted, start = 1):
            current = row[index]
            row[index] = previous + 1 if expected_token == predicted_token else max(row[index], row[index - 1])
            previous = current
    length = row[-1]
    if not length:
        return 0.0
    precision = length / len(predicted)
    recall = length / len(expected)
    return 2 * precision * recall / (precision + recall)


def ngrams(*, tokens: list[str], order: int) -> Counter:
    """Считает n-граммы заданной длины.

    Аргументы:
        tokens: токены строки.
        order: длина n-граммы.

    Возвращает:
        Счётчик n-грамм.
    """
    return Counter(
        tuple(tokens[start:start + order]) for start in range(len(tokens) - order + 1)
    )


def cider_frequencies(*, references: list[str]) -> tuple[dict[int, Counter], int]:
    """Считает, в скольких эталонах встречается каждая n-грамма.

    Аргументы:
        references: эталонные строки выборки.

    Возвращает:
        Частоты по длинам n-грамм и число эталонов.
    """
    frequencies = {order: Counter() for order in CIDER_ORDERS}
    for reference in references:
        tokens = tokens_of(text = reference)
        for order in CIDER_ORDERS:
            frequencies[order].update(set(ngrams(tokens = tokens, order = order)))
    return frequencies, len(references)


def cider_vector(*, tokens: list[str], order: int, frequencies: Counter, total: int) -> dict:
    """Строит вектор tf-idf по n-граммам одной длины.

    Аргументы:
        tokens: токены строки.
        order: длина n-граммы.
        frequencies: в скольких эталонах встречается каждая n-грамма.
        total: число эталонов.

    Возвращает:
        Соответствие «n-грамма - вес».
    """
    import math

    counts = ngrams(tokens = tokens, order = order)
    length = sum(counts.values()) or 1
    vector = {}
    for gram, count in counts.items():
        document_frequency = frequencies.get(gram, 0)
        idf = math.log(max(total, 1) / max(document_frequency, 1))
        vector[gram] = count / length * idf
    return vector


def cosine(*, left: dict, right: dict) -> float:
    """Считает косинус между двумя разреженными векторами.

    Аргументы:
        left: первый вектор.
        right: второй вектор.

    Возвращает:
        Значение от нуля до единицы.
    """
    import math

    if not left or not right:
        return 0.0
    dot = sum(weight * right.get(gram, 0.0) for gram, weight in left.items())
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def cider(*, prediction: str, reference: str, frequencies: dict[int, Counter], total: int) -> float:
    """Считает CIDEr: косинус tf-idf по n-граммам, усреднённый по длинам.

    Аргументы:
        prediction: ответ модели.
        reference: эталон.
        frequencies: частоты n-грамм по выборке эталонов.
        total: число эталонов.

    Возвращает:
        Значение от нуля до единицы.
    """
    predicted = tokens_of(text = prediction)
    expected = tokens_of(text = reference)
    scores = []
    for order in CIDER_ORDERS:
        left = cider_vector(
            tokens = predicted, order = order, frequencies = frequencies[order], total = total
        )
        right = cider_vector(
            tokens = expected, order = order, frequencies = frequencies[order], total = total
        )
        scores.append(cosine(left = left, right = right))
    return sum(scores) / len(scores)


def score(*, predictions: list[str], references: list[str]) -> dict[str, float]:
    """Считает средние текстовые метрики по выборке.

    Аргументы:
        predictions: ответы модели.
        references: эталоны в том же порядке.

    Возвращает:
        Среднее по каждой метрике.
    """
    if len(predictions) != len(references):
        raise ValueError(f"ответов {len(predictions)}, а эталонов {len(references)}")
    if not predictions:
        return {name: 0.0 for name in ("exact", "token_f1", "bleu", "nist", "meteor", "rouge_l", "cider")}

    frequencies, total = cider_frequencies(references = references)
    sums = Counter()
    for prediction, reference in zip(predictions, references):
        predicted = tokens_of(text = prediction)
        expected = tokens_of(text = reference)
        sums["exact"] += prediction.strip() == reference.strip()
        sums["token_f1"] += token_f1(prediction = prediction, reference = reference)
        sums["rouge_l"] += rouge_l(prediction = prediction, reference = reference)
        sums["cider"] += cider(
            prediction = prediction, reference = reference, frequencies = frequencies, total = total
        )
        sums["bleu"] += sentence_bleu(
            [expected], predicted, weights = (0.25, 0.25, 0.25, 0.25), smoothing_function = SMOOTHING
        )
        # nist падает на коротких строках, где не набирается ни одной общей n-граммы.
        try:
            sums["nist"] += sentence_nist([expected], predicted)
        except (ZeroDivisionError, ValueError):
            pass
        sums["meteor"] += meteor_score([expected], predicted, wordnet = NO_WORDNET)

    return {name: value / len(predictions) for name, value in sums.items()}
