"""Генерация ответов модели на вопросы датасета.

Ответ модели проходит через `extract_query`: из текста берётся строка запроса,
обрамление кода и пояснения вокруг отбрасываются. Отбрасывается только форма;
выдумал ли модель чужой язык, решает метрика.
"""

import re

import torch
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from ecql_dataset.ecql.grammar import EcqlError, START_KEYWORD
from ecql_dataset.prompt import build_messages

# Потолок длины ответа. Самый длинный эталон датасета - четыре условия с
# суффиксом, это меньше сотни токенов; запас нужен на неудачный ответ, который
# иначе оборвётся и станет неразбираемым вместо того, чтобы честно попасть в
# ошибку.
MAX_NEW_TOKENS = 128

# Начало блока рассуждений Qwen3. Рассуждение выключено параметром шаблона;
# появилось - значит шаблон вызван не так, как в обучении.
THINKING_MARK = "<think>"

# Обрамление кода в ответе.
FENCE_PATTERN = re.compile(r"^```[a-z]*|```$", flags = re.MULTILINE)


def load_model(*, model_name: str, dtype: torch.dtype, load_in_4bit: bool) -> tuple:
    """Загружает модель и токенизатор.

    Аргументы:
        model_name: имя модели на HuggingFace.
        dtype: тип весов при загрузке без квантования.
        load_in_4bit: грузить ли базу в четырёх битах; на Apple Silicon
            недоступно, там bitsandbytes не работает.

    Возвращает:
        Пару «модель, токенизатор».
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Дополнение слева: у модели-декодера продолжение пишется от последнего
    # токена, и дополнение справа оторвало бы его от вопроса.
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    arguments = {"dtype": dtype}
    if load_in_4bit:
        arguments["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit = True,
            bnb_4bit_quant_type = "nf4",
            bnb_4bit_compute_dtype = dtype,
            bnb_4bit_use_double_quant = True,
        )
        arguments["device_map"] = "auto"

    model = AutoModelForCausalLM.from_pretrained(model_name, **arguments)
    model.eval()
    return model, tokenizer


def render_prompt(*, tokenizer, instruction: str, question: str) -> str:
    """Собирает строку запроса к модели по шаблону чата (выделено в метод, чтобы параметры были всегда одни и те же).

    Аргументы:
        tokenizer: токенизатор модели.
        instruction: текст инструкции.
        question: вопрос человека.

    Возвращает:
        Строку запроса, оборванную на начале ответа ассистента.
    """
    return tokenizer.apply_chat_template(
        build_messages(instruction = instruction, question = question),
        tokenize = False,
        add_generation_prompt = True,
        enable_thinking = False,
    )


def extract_query(*, answer: str) -> str:
    """Достаёт строку запроса из ответа модели.

    Аргументы:
        answer: текст ответа.

    Возвращает:
        Строку запроса; ответ без запроса возвращается первой непустой строкой,
        чтобы метрика увидела то, что модель написала на самом деле.

    Роняет:
        EcqlError: ответ содержит рассуждение, шаблон чата вызван неверно.
    """
    if THINKING_MARK in answer:
        raise EcqlError(
            "модель ответила рассуждением: шаблон чата вызван без enable_thinking = False"
        )
    text = FENCE_PATTERN.sub("", answer)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines:
        if line.startswith(START_KEYWORD):
            return line
    return lines[0] if lines else ""


def generate(
    *,
    model,
    tokenizer,
    questions: list[str],
    instruction: str,
    batch_size: int,
    max_new_tokens: int = MAX_NEW_TOKENS,
    progress: bool = True,
) -> list[str]:
    """Генерирует ответы на вопросы.

    Greedy decoding, do_sample=False.
     На каждом шаге модель даёт вероятности всех токенов; жадный выбор берёт самый вероятный и идёт дальше.

    Аргументы:
        model: загруженная модель.
        tokenizer: токенизатор модели.
        questions: вопросы человека.
        instruction: текст инструкции, общий для всех вопросов.
        batch_size: сколько вопросов подаётся за раз.
        max_new_tokens: потолок длины ответа.
        progress: показывать ли полосу прогресса по батчам.

    Возвращает:
        Строки запросов в порядке вопросов.
    """
    answers: list[str] = []
    starts = range(0, len(questions), batch_size)
    for start in tqdm(starts, desc = "генерация", unit = "батч", disable = not progress):
        batch = questions[start:start + batch_size]
        prompts = [
            render_prompt(tokenizer = tokenizer, instruction = instruction, question = question)
            for question in batch
        ]
        encoded = tokenizer(prompts, return_tensors = "pt", padding = True).to(model.device)
        with torch.no_grad():
            produced = model.generate(
                **encoded,
                max_new_tokens = max_new_tokens,
                do_sample = False,
                pad_token_id = tokenizer.pad_token_id,
            )
        # Оставляем только дописанное: длина запроса в батче общая после дополнения.
        written = produced[:, encoded["input_ids"].shape[1]:]
        for text in tokenizer.batch_decode(written, skip_special_tokens = True):
            answers.append(extract_query(answer = text))
    return answers
