# ECQL: DSL Query Generator

Домашнее задание «DSL Query Generator», курс «LLM-инженер».

Сущности задания переотображены на реальную базу КМВ (курорты Кавминвод): вместо
вымышленной компании — места, отзывы, соседство объектов и цены проезда.

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
- `@price_kind` — средний чек, цена за ночь
- `@object_kind` — памятник, ансамбль, достопримечательное место
- `@heritage_status` — федеральный, региональный, местный
- `@wheelchair` — да, нет, частично

`[REVIEWS]`
- `@name` — Жемчужина, Hotel Verona, Espero, Особняк
- `@city` — Кисловодск, Пятигорск, Ессентуки, Железноводск
- `@object_class` — отель, гостевой дом, санаторий, хостел
- `@rating` — 1, 2, 3, 4, 5
- `@aspects` — номер, расположение, завтрак, персонал, чистота, бассейн и спа, цена, шум, wi-fi, парковка; от одного до четырёх значений через запятую, фильтр через `CONTAINS`

`[PROXIMITY]`
- `@name` — имя объекта-якоря; производное от `[PLACES]` по `place_id`
- `@neighbour_category` — те же значения, что у `@category`
- `@distance_m` — 86, 104, 500, 1500

`[FARES]`
- `@transport` — самолёт, автобус, поезд, трамвай
- `@route_start` — Минеральные Воды, Кисловодск, Пятигорск, Москва
- `@route_end` — Москва, Санкт-Петербург, Сочи, Кисловодск
- `@fare_class` — эконом, бизнес, плацкарт, купе
- `@price_rub` — 30, 35, 8090, 23110

Полная спецификация языка — [docs/dz_ECQL.md](docs/dz_ECQL.md).

# Отличия от правил ДЗ

- Добавлены операторы `CONTAINS` и `NOT CONTAINS` для строковых полей.
- Суффикс вывода (`AS JSON`, `AS TABLE`, `AS LIST`) ставится только тогда, когда
  человек назвал формат словами; иначе не пишется.
- Вложенность спецификацией ДЗ не определена, поэтому сложность выражена числом
  условий от одного до четырёх.

# Структура

```
dataset/ecql/
  vocabulary.json   значения полей, выгруженные из csv КМВ
  slots.json        261 слот: сущность, условия, связка, суффикс, готовая строка ECQL
  places.md         рабочие листы: вопрос на русском + ECQL + строка разметки
  reviews.md
  proximity.md
  fares.md
src/ecql_dataset/
  schema.py         сущности, поля, типы, допустимые операторы
  vocabulary.py     csv КМВ  → vocabulary.json
  planner.py        vocabulary.json → slots.json по квотам осей
  sheets.py         slots.json → md-листы; написанные вопросы переносятся
docs/
  dz_ECQL_task.md      постановка ДЗ
  dz_ECQL.md           спецификация языка и схема данных
  dz_ECQL_dataset.md   состав датасета, пороги покрытия, протокол оценки
  example/             референсный notebook LoRA с другого домена
```

# Цепочка сборки

```
csv КМВ ──vocabulary.py──▶ vocabulary.json ──planner.py──▶ slots.json
   ──sheets.py──▶ *.md ──человек пишет вопросы──▶ *.md ──сборщик──▶ jsonl
```

```bash
python -m ecql_dataset.vocabulary --dataset-root <kmv-dataset>/data/dataset \
    --output dataset/ecql/vocabulary.json
python -m ecql_dataset.planner --vocabulary dataset/ecql/vocabulary.json \
    --output dataset/ecql/slots.json
python -m ecql_dataset.sheets --slots dataset/ecql/slots.json \
    --directory dataset/ecql
```

Правится руками только вопрос на русском в md-листах. Строка ECQL и разметка
под ней выводятся из слота; перезапуск генератора вопросы сохраняет.

Состояние: 261 пара, вопросы написаны. Сборщик `md → train/val/test.jsonl` и
`coverage.md` не написан; `challenge.md` не написан.

В репозитории только вспомогательный код сборки датасета. Обучение, метрики и
выводы — в notebook.

# Notebook

TODO обучение, сравнение прогонов, метрики, выводы, ссылка на веса адаптера
