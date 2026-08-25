# ECQL: DSL Query Generator

Домашнее задание «DSL Query Generator», курс «LLM-инженер».

По заданию описывались правила вымышленного корпоративного языка запросов ECQL, который используется в компании «E-Corp».
Основные сущности: [EMPLOYEES], [PROJECTS], [INVENTORY], [DEALS] и поля для них вроде: @salary, @status, @city

Корпоративная БД про работников - это скучно и не интересно. Сохранил правила языка но предметную область взял: путеводитель по местам и городам КавМинВод.

Вместо вымышленной компании — места, отзывы, соседство объектов и цены проезда.

| Сущность ДЗ | Здесь | Таблица КМВ | Строк |
|---|---|---|---|
| `[EMPLOYEES]` | `[PLACES]` | `places/places.csv` | 2642 |
| `[INVENTORY]` | `[REVIEWS]` | `places/reviews.csv` | 791 |
| `[PROJECTS]` | `[PROXIMITY]` | `places/proximity.csv` | 45055 |
| `[DEALS]` | `[FARES]` | `transit/leg_prices.csv` | 1451 |

# Схема данных

`[PLACES]`
- `@name` — Нарзанная галерея, Провал, Курортный парк, Краеведческий музей
- `@city` — Кисловодск, Пятигорск, Ессентуки, Минеральные Воды, Железноводск, Иноземцево, Лермонтов, вне городов
- `@category` — culture, food, shopping, lodging, nature, service, water, activity, transport
- `@price_rub` — 200, 300, 500, 1300
- `@price_kind` — average_check, per_night
- `@object_kind` — monument, ensemble, heritage_site
- `@heritage_status` — federal, regional, local
- `@wheelchair` — yes, no, limited

`[REVIEWS]`
- `@name` — Жемчужина, Hotel Verona, Espero, Особняк
- `@city` — Кисловодск, Пятигорск, Ессентуки, Железноводск
- `@object_class` — hotel, guesthouse, sanatorium, hostel
- `@rating` — 1, 2, 3, 4, 5
- `@aspects` — номер, расположение, завтрак, персонал, чистота, бассейн и спа, цена, шум, wi-fi, парковка; от одного до четырёх значений через запятую, фильтр через `CONTAINS`

`[PROXIMITY]`
- `@name` — имя объекта (те же что в PLACES)
- `@neighbour_category` — те же значения, что у `@category`
- `@distance_m` — 86, 104, 500, 1500

`[FARES]`
- `@transport` — plane, bus, train, tram
- `@route_start` — Минеральные Воды, Кисловодск, Пятигорск, Москва
- `@route_end` — Москва, Санкт-Петербург, Сочи, Кисловодск
- `@fare_class` — economy, business, platskart, kupe
- `@price_rub` — 30, 35, 8090, 23110


# Отличия от правил ДЗ

- Добавлены операторы `CONTAINS` и `NOT CONTAINS` для строковых полей.
- Вложенность спецификацией ДЗ не определена, поэтому сложность выражена числом
  условий от одного до четырёх (через && или ||).
- Правила языка не вводят понятия группировки операций (нет скобок), я не добавлял чтобы не усложнять. Считаю что операторы && и || одновременно запрещены.

# Как собирался датасет

Есть локальный датасет собранный самостоятельно для городов, объектов, маршрутов транспорта Кавказских Минеральных Вод.

Claude Code:
- собрал из него необходимые словари сущностей
- сгенерировал листы-заготовки ([places.md](dataset/ecql/source/places.md), [reviews.md](dataset/ecql/source/reviews.md), [proximity.md](dataset/ecql/source/proximity.md), [fares.md](dataset/ecql/source/fares.md)): на каждую сущность готовый набор ECQL-запросов, покрывающий все правила языка
- дополнительно был написан md-лист со "сложными" неоднозначными вопросами ([challenge.md](dataset/ecql/source/challenge.md))
- после генерации заготовок md-листов сгенерировал на основе ECQL-запросов запросы на человеческом языке
- т.к. качество вопросов получилось не очень (короткие/странные/канцелярские) дополнительно был прогнан саб агент по всем вопросам батчем по 10 и переформулировал их в более естественные
- написал скрипт-билдер для сборки из md-листов jsonl-файлов и разложил их на пары на train, val и test.

Итого 276 пар: train 176, val 32, test 68.

В 68 тестовых вошли также 15 вопросов из [challenge.md](dataset/ecql/source/challenge.md)

Итоговая цепочка сборки:

```
csv КМВ (вне проекта) ── vocabulary.py ──▶ vocabulary.json ── planner.py ──▶ slots.json
   ── sheets.py ──▶ *.md ── человек пишет вопросы ──▶ *.md ── builder.py ──▶ jsonl
```

Описывать и отчитывать по скриптам сборки датасета не буду - т.к. это не основная часть работы.

Как собрать jsonl из готовых md файлов:

```bash
uv run python -m ecql_dataset.build.builder --source dataset/ecql/source --output dataset/ecql \
    --vocabulary dataset/ecql/source/vocabulary.json \
    --glossary dataset/ecql/source/enum_glossary.json
```

# Структура файлов проекта

```
dataset/ecql/          датасет: то, что грузится в обучение
  train.jsonl
  val.jsonl
  test.jsonl
  coverage.md          отчёт покрытия по осям

  source/              кухня: из чего датасет собран
    vocabulary.json    значения полей из учебного датасета по КМВ; источник для
                       генератора, валидатора и схемы в промпте
    slots.json         слоты — заготовки пар: готовый ECQL, под который человек пишет вопрос
    
    places.md          датасет в человекочитаемом виде, по файлу на сущность;
                       вопрос пишет человек, ECQL готовый
    reviews.md
    proximity.md
    fares.md
    
    challenge.md       15 трудных примеров, написаны вручную; только для доп проверки обученной модели

src/ecql_dataset/    исходники

  prompt.py          собирает промпты из словаря и схемы: короткий для обучения,
                     полный с правилами языка для базовой модели

  ecql/              проверка языка — едет в ноутбук
    schema.py        какие поля есть у каждой сущности, какие операторы им разрешены,
                     как записывается значение
    grammar.py       разбирает строку ECQL на части: сравнить ответ модели с эталоном
                     по смыслу, а не по буквам, и поймать ответ, который не ECQL
    validate.py      проверка запроса по схеме и данным
    
  build/             создаёт датасет; после сборки не нужен
    vocabulary.py
    planner.py
    sheets.py
    builder.py

  notebook/          код ноутбука
    generate.py      загрузка модели, генерация ответов, вырезание запроса из ответа
    eval/
      product.py     метрики по смыслу запроса плюс самопроверка эвалюатора
      text.py        текстовые метрики: exact, token_f1, bleu, meteor, rouge_l, cider

```

# Notebook

Тут — [notebook/ecql_lora.ipynb](notebook/ecql_lora.ipynb).

# Отчет по вопросам ДЗ 

Тут — [docs/REPORT.md](docs/REPORT.md).

