# Покрытие датасета ECQL

Отчёт собирается `ecql_dataset.builder`; руками не правится.

| Сплит | Строк |
|---|---|
| train | 176 |
| val | 32 |
| test | 68 |
| в том числе challenge | 15 |

## Сущность

| Значение | train | val | test | всего |
|---|---|---|---|---|
| PLACES | 64 | 12 | 25 | 101 |
| REVIEWS | 45 | 8 | 17 | 70 |
| PROXIMITY | 38 | 6 | 14 | 58 |
| FARES | 29 | 6 | 12 | 47 |

## Число условий

| Значение | train | val | test | всего |
|---|---|---|---|---|
| 2 | 63 | 12 | 27 | 102 |
| 3 | 54 | 10 | 19 | 83 |
| 1 | 36 | 6 | 15 | 57 |
| 4 | 23 | 4 | 7 | 34 |

## Связка

| Значение | train | val | test | всего |
|---|---|---|---|---|
| && | 125 | 23 | 46 | 194 |
| нет | 36 | 6 | 15 | 57 |
| || | 15 | 3 | 7 | 25 |

## Суффикс вывода

| Значение | train | val | test | всего |
|---|---|---|---|---|
| нет | 130 | 25 | 47 | 202 |
| LIST | 19 | 3 | 10 | 32 |
| TABLE | 14 | 3 | 9 | 26 |
| JSON | 13 | 1 | 2 | 16 |

## Оператор

| Значение | train | val | test | всего |
|---|---|---|---|---|
| IS | 168 | 28 | 62 | 258 |
| BELOW | 46 | 6 | 14 | 66 |
| ABOVE | 36 | 6 | 8 | 50 |
| CONTAINS | 25 | 7 | 12 | 44 |
| NOT | 23 | 4 | 7 | 34 |
| NOT CONTAINS | 15 | 1 | 4 | 20 |

## Поле

| Значение | train | val | test | всего |
|---|---|---|---|---|
| PLACES.@category | 30 | 8 | 14 | 52 |
| PROXIMITY.@neighbour_category | 36 | 5 | 11 | 52 |
| REVIEWS.@aspects | 32 | 7 | 13 | 52 |
| PROXIMITY.@distance_m | 25 | 5 | 10 | 40 |
| PLACES.@price_rub | 23 | 4 | 4 | 31 |
| PLACES.@city | 15 | 5 | 10 | 30 |
| REVIEWS.@rating | 21 | 2 | 7 | 30 |
| PLACES.@name | 18 | 4 | 6 | 28 |
| REVIEWS.@object_class | 18 | 5 | 4 | 27 |
| FARES.@transport | 12 | 4 | 8 | 24 |
| PROXIMITY.@name | 15 | 2 | 7 | 24 |
| FARES.@fare_class | 15 | 3 | 5 | 23 |
| FARES.@price_rub | 16 | 2 | 5 | 23 |
| PLACES.@price_kind | 14 | 3 | 5 | 22 |
| FARES.@route_end | 14 | 2 | 5 | 21 |
| FARES.@route_start | 12 | 2 | 5 | 19 |
| PLACES.@object_kind | 11 | 2 | 4 | 17 |
| PLACES.@heritage_status | 11 | 1 | 4 | 16 |
| PLACES.@wheelchair | 9 | 2 | 5 | 16 |
| REVIEWS.@city | 13 | 1 | 2 | 16 |
| REVIEWS.@name | 8 | 1 | 3 | 12 |

## Нарушенные пороги

Нет.
