# PROXIMITY

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Назови места, у которых по соседству есть кафе или столовая.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food'
  # слот 29 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- У каких мест под боком остановка?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport'
  # слот 40 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Чем заняться рядом?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity'
  # слот 126 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Перечисли места, рядом с которыми есть отель или гостевой дом
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging'
  # слот 135 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- У каких мест по соседству есть источники и бюветы? Ответ в json
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' AS JSON
  # слот 139 · одно условие · без связки · AS JSON · предмет назван · поля @neighbour_category · операторы IS

- Какие услуги рядом?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service'
  # слот 140 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Рядом с какими местами есть спортзал, бассейн или стадион? Ответ в json.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' AS JSON
  # слот 164 · одно условие · без связки · AS JSON · предмет назван · поля @neighbour_category · операторы IS

- Какие места стоят рядом с чем-то культурным?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture'
  # слот 176 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Подскажи места, по соседству с которыми есть источник или бювет.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water'
  # слот 178 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Какие соседи оказались дальше 60 метров?
  → FETCH [PROXIMITY] WHERE @distance_m ABOVE 60
  # слот 243 · одно условие · без связки · без суффикса · поля @distance_m · операторы ABOVE

- Что рядом с Домом Разумовского В. И.?
  → FETCH [PROXIMITY] WHERE @name IS 'Дом Разумовского В. И.'
  # слот 255 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

## Два условия

- Ищу места, у которых спортзал или бассейн по соседству не дальше 170 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' && @distance_m BELOW 170
  # слот 19 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- У каких мест по соседству кафе или парк?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food' || @neighbour_category IS 'nature'
  # слот 20 · 2 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Перечисли списком места, где галерея или терренкур не дальше 800 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service' && @distance_m BELOW 800 AS LIST
  # слот 25 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Где переночевать рядом с объектом «В этом доме жил Умар Джашуевич Алиев»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging' && @name IS 'В этом доме жил Умар Джашуевич Алиев'
  # слот 72 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @name · операторы IS

- Где поесть рядом с «Арабикой»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food' && @name IS 'Арабика'
  # слот 118 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @name · операторы IS

- Перечисли списком места, у которых вокзал в пределах 300 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport' && @distance_m BELOW 300 AS LIST
  # слот 133 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- У каких мест терренкур или галерея по соседству дальше 200 метров?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service' && @distance_m ABOVE 200
  # слот 138 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- У каких мест по соседству есть парк, сквер или озеро не дальше 1100 метров? Ответ списком.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'nature' && @distance_m BELOW 1100 AS LIST
  # слот 143 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- В таблице покажи места, у которых музей дальше 600 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' && @distance_m ABOVE 600 AS TABLE
  # слот 153 · 2 условия · && · AS TABLE · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Ищу места, у которых терренкур или станция маршрута в пределах 300 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service' && @distance_m BELOW 300
  # слот 156 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Рядом магазины или культура
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' || @neighbour_category IS 'culture'
  # слот 159 · 2 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Ищу места, у которых кафе в пределах 20 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food' && @distance_m BELOW 20
  # слот 166 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Подскажи объекты, у которых отель по соседству дальше 100 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging' && @distance_m ABOVE 100
  # слот 168 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Покажи в таблице места, у которых музей или церковь в пределах 700 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' && @distance_m BELOW 700 AS TABLE
  # слот 174 · 2 условия · && · AS TABLE · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Отбери места, от которых до бювета меньше 500 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m BELOW 500
  # слот 188 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Списком перечисли места, от которых до родника больше 400 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m ABOVE 400 AS LIST
  # слот 191 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Какие объекты стоят от «Ventuno» дальше 600 метров?
  → FETCH [PROXIMITY] WHERE @name IS 'Ventuno' && @distance_m ABOVE 600
  # слот 210 · 2 условия · && · без суффикса · предмет назван · поля @name @distance_m · операторы IS ABOVE

- Что стоит в пределах 400 метров от Храма Смоленской иконы Божией Матери, списком.
  → FETCH [PROXIMITY] WHERE @name IS 'Храм Смоленской иконы Божией Матери' && @distance_m BELOW 400 AS LIST
  # слот 221 · 2 условия · && · AS LIST · предмет назван · поля @name @distance_m · операторы IS BELOW

- Гулять хочу в зелени: у каких мест парк или сквер по соседству в пределах 800 метров?
  → FETCH [PROXIMITY] WHERE @distance_m BELOW 800 && @neighbour_category IS 'nature'
  # слот 222 · 2 условия · && · без суффикса · предмет назван · поля @distance_m @neighbour_category · операторы BELOW IS

- Назови соседей Особняка Милашевских, до которых больше 70 метров.
  → FETCH [PROXIMITY] WHERE @name IS 'Особняк Милашевских' && @distance_m ABOVE 70
  # слот 223 · 2 условия · && · без суффикса · предмет назван · поля @name @distance_m · операторы IS ABOVE

- Нужны места, где сосед стоит дальше 200 метров и это не музей.
  → FETCH [PROXIMITY] WHERE @distance_m ABOVE 200 && @neighbour_category NOT 'culture'
  # слот 225 · 2 условия · && · без суффикса · предмет назван · поля @distance_m @neighbour_category · операторы ABOVE NOT

- Покажи, что попадает в 1200 метров от «Palazzo».
  → FETCH [PROXIMITY] WHERE @name IS 'Palazzo' && @distance_m BELOW 1200
  # слот 235 · 2 условия · && · без суффикса · предмет назван · поля @name @distance_m · операторы IS BELOW

- У каких мест музей, церковь или памятник по соседству дальше 1300 метров?
  → FETCH [PROXIMITY] WHERE @distance_m ABOVE 1300 && @neighbour_category IS 'culture'
  # слот 242 · 2 условия · && · без суффикса · предмет назван · поля @distance_m @neighbour_category · операторы ABOVE IS

## Три условия

- Собираю маршрут: нужны места, по соседству с которыми есть музей, парк или терренкур, одним списком.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' || @neighbour_category IS 'nature' || @neighbour_category IS 'service' AS LIST
  # слот 39 · 3 условия · || · AS LIST · предмет назван · поля @neighbour_category · операторы IS

- Какие места стоят по соседству с супермаркетом, автовокзалом или гостевым домом?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' || @neighbour_category IS 'transport' || @neighbour_category IS 'lodging'
  # слот 42 · 3 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Найди места, рядом с которыми парк, сквер или озеро дальше 1000 метров, но ближе 1500 метров. Покажи таблицей
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'nature' && @distance_m ABOVE 1000 && @distance_m BELOW 1500 AS TABLE
  # слот 45 · 3 условия · && · AS TABLE · диапазон · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE BELOW

- Найди места, у которых бассейн на расстоянии от 160 до 180 метров.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' && @distance_m ABOVE 160 && @distance_m BELOW 180
  # слот 49 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE BELOW

- Покажи вокзалы и аэропорты в пределах 140 метров от памятника «В.И. Ленину», списком.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport' && @name IS 'В.И. Ленину' && @distance_m BELOW 140 AS LIST
  # слот 83 · 3 условия · && · AS LIST · предмет назван · поля @neighbour_category @name @distance_m · операторы IS BELOW

- Перечисли супермаркеты дальше 130 метров от «Ресторана Парк».
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' && @name IS 'Ресторан Парк' && @distance_m ABOVE 130
  # слот 112 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @name @distance_m · операторы IS ABOVE

- Какие вокзалы и автовокзалы стоят дальше 120 метров от памятника «В.И. Ленину»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport' && @name IS 'В.И. Ленину' && @distance_m ABOVE 120
  # слот 115 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @name @distance_m · операторы IS ABOVE

- Нужна таблица: какие музеи и церкви ближе 700 метров от «Мини отеля»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' && @name IS 'Мини отель' && @distance_m BELOW 700 AS TABLE
  # слот 124 · 3 условия · && · AS TABLE · предмет назван · поля @neighbour_category @name @distance_m · операторы IS BELOW

- Покажи в json отели и гостевые дома в пределах 110 метров от объекта «В этом доме жил Умар Джашуевич Алиев».
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging' && @distance_m BELOW 110 && @name IS 'В этом доме жил Умар Джашуевич Алиев' AS JSON
  # слот 130 · 3 условия · && · AS JSON · предмет назван · поля @neighbour_category @distance_m @name · операторы IS BELOW

- Что из спортзалов и бассейнов стоит дальше 160 метров от Творческой студии «Время творить»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' && @name IS 'Творческая студия «Время творить»' && @distance_m ABOVE 160
  # слот 165 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @name @distance_m · операторы IS ABOVE

- Стою у «Ресторана Парк» — какие магазины дальше 130 метров?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' && @distance_m ABOVE 130 && @name IS 'Ресторан Парк'
  # слот 167 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m @name · операторы IS ABOVE

- Какие магазины стоят не дальше 140 метров от «Ресторана Парк»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' && @distance_m BELOW 140 && @name IS 'Ресторан Парк'
  # слот 170 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m @name · операторы IS BELOW

- У «DunCan Lounge» — какие соседи дальше 200 метров, ночлег не в счёт?
  → FETCH [PROXIMITY] WHERE @name IS 'DunCan Lounge' && @distance_m ABOVE 200 && @neighbour_category NOT 'lodging'
  # слот 200 · 3 условия · && · без суффикса · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

- Ищу, что соседствует с антикафе «Песочница» дальше 1100 метров, и ночлег мне не нужен.
  → FETCH [PROXIMITY] WHERE @name IS 'Антикафе "Песочница"' && @distance_m ABOVE 1100 && @neighbour_category NOT 'lodging'
  # слот 201 · 3 условия · && · без суффикса · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

- Культура, природа или жильё рядом
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' || @neighbour_category IS 'nature' || @neighbour_category IS 'lodging'
  # слот 203 · 3 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Выведи в json объекты дальше 180 метров от «Суши хаус», бассейны и спортзалы пропусти.
  → FETCH [PROXIMITY] WHERE @name IS 'Суши хаус' && @distance_m ABOVE 180 && @neighbour_category NOT 'activity' AS JSON
  # слот 224 · 3 условия · && · AS JSON · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

- Списком покажи места, у которых по соседству есть магазин, кафе или парк.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' || @neighbour_category IS 'food' || @neighbour_category IS 'nature' AS LIST
  # слот 236 · 3 условия · || · AS LIST · предмет назван · поля @neighbour_category · операторы IS

- Дай таблицей соседей Ансамбля лютеранской кирхи в пределах 190 метров, бассейны и спортзалы пропусти.
  → FETCH [PROXIMITY] WHERE @name IS 'Ансамбль лютеранской кирхи' && @distance_m BELOW 190 && @neighbour_category NOT 'activity' AS TABLE
  # слот 251 · 3 условия · && · AS TABLE · предмет назван · поля @name @distance_m @neighbour_category · операторы IS BELOW NOT

- Интересует всё, что удалено от Колодца желаний больше чем на 110 метров, ночлег не предлагай.
  → FETCH [PROXIMITY] WHERE @name IS 'Колодец желаний' && @distance_m ABOVE 110 && @neighbour_category NOT 'lodging'
  # слот 258 · 3 условия · && · без суффикса · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

## Четыре условия

- Ищу парки и озёра от «Второго деда» дальше 1000 метров, но ближе 1200 метров — списком.
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'nature' && @distance_m ABOVE 1000 && @distance_m BELOW 1200 && @name IS 'Второй дед' AS LIST
  # слот 12 · 4 условия · && · AS LIST · диапазон · предмет назван · поля @neighbour_category @distance_m @name · операторы IS ABOVE BELOW

- Какие источники и бюветы у памятника «А. С. Пушкин» стоят дальше 90 метров, но ближе 120 метров?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m ABOVE 90 && @distance_m BELOW 120 && @name IS 'А. С. Пушкин'
  # слот 52 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @neighbour_category @distance_m @name · операторы IS ABOVE BELOW
