# FARES

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Что есть в бизнес-классе?
  → FETCH [FARES] WHERE @fare_class IS 'business'
  # слот 9 · одно условие · без связки · без суффикса · предмет назван · поля @fare_class · операторы IS

- В json собери тарифы на автобусные рейсы
  → FETCH [FARES] WHERE @transport IS 'bus' AS JSON
  # слот 58 · одно условие · без связки · AS JSON · предмет назван · поля @transport · операторы IS

- Что в экономе?
  → FETCH [FARES] WHERE @fare_class IS 'economy'
  # слот 80 · одно условие · без связки · без суффикса · предмет назван · поля @fare_class · операторы IS

- Интересует плацкарт - покажи цены на такие билеты.
  → FETCH [FARES] WHERE @fare_class IS 'platskart'
  # слот 94 · одно условие · без связки · без суффикса · предмет назван · поля @fare_class · операторы IS

- Дай таблицу с ценами на трамвайный проезд.
  → FETCH [FARES] WHERE @transport IS 'tram' AS TABLE
  # слот 141 · одно условие · без связки · AS TABLE · предмет назван · поля @transport · операторы IS

- Собираюсь в Казань — покажи цены на билеты туда.
  → FETCH [FARES] WHERE @route_end IS 'Казань'
  # слот 190 · одно условие · без связки · без суффикса · предмет назван · поля @route_end · операторы IS

- Рейсы до Самары — дай json
  → FETCH [FARES] WHERE @route_end IS 'Самара' AS JSON
  # слот 219 · одно условие · без связки · AS JSON · предмет назван · поля @route_end · операторы IS

- Что отправляется из Санкт-Петербурга?
  → FETCH [FARES] WHERE @route_start IS 'Санкт-Петербург'
  # слот 229 · одно условие · без связки · без суффикса · предмет назван · поля @route_start · операторы IS

## Два условия

- Еду поездом в плацкарте, покажи тарифы.
  → FETCH [FARES] WHERE @fare_class IS 'platskart' && @transport IS 'train'
  # слот 14 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @transport · операторы IS

- Перечисли автобусные рейсы дороже 30 рублей.
  → FETCH [FARES] WHERE @transport IS 'bus' && @price_rub ABOVE 30
  # слот 15 · 2 условия · && · без суффикса · предмет назван · поля @transport @price_rub · операторы IS ABOVE

- Полечу самолётом в экономе — покажи цены.
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @transport IS 'plane'
  # слот 59 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @transport · операторы IS

- Назови цены на бизнес-класс в самолётах.
  → FETCH [FARES] WHERE @fare_class IS 'business' && @transport IS 'plane'
  # слот 67 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @transport · операторы IS

- Автобусы до Кисловодска, покажи таблицей
  → FETCH [FARES] WHERE @transport IS 'bus' && @route_end IS 'Кисловодск' AS TABLE
  # слот 132 · 2 условия · && · AS TABLE · предмет назван · поля @transport @route_end · операторы IS

- Списком выдай цены на трамвай из Пятигорска.
  → FETCH [FARES] WHERE @transport IS 'tram' && @route_start IS 'Пятигорск' AS LIST
  # слот 145 · 2 условия · && · AS LIST · предмет назван · поля @transport @route_start · операторы IS

- Уезжаю из Минеральных Вод — покажи тарифы эконом-класса.
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @route_start IS 'Минеральные Воды'
  # слот 152 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @route_start · операторы IS

- Интересует бизнес-класс — нужны билеты дороже 23000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'business' && @price_rub ABOVE 23000
  # слот 171 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @price_rub · операторы IS ABOVE

- Какие есть рейсы до Екатеринбурга дороже 28000 рублей?
  → FETCH [FARES] WHERE @route_end IS 'Екатеринбург' && @price_rub ABOVE 28000
  # слот 195 · 2 условия · && · без суффикса · предмет назван · поля @route_end @price_rub · операторы IS ABOVE

- Собираюсь в Нижний Новгород, подбери билеты дешевле 27000 рублей — списком.
  → FETCH [FARES] WHERE @price_rub BELOW 27000 && @route_end IS 'Нижний Новгород' AS LIST
  # слот 205 · 2 условия · && · AS LIST · предмет назван · поля @price_rub @route_end · операторы BELOW IS

- Какие тарифы бывают на самолёт или поезд?
  → FETCH [FARES] WHERE @transport IS 'plane' || @transport IS 'train'
  # слот 209 · 2 условия · || · без суффикса · предмет назван · поля @transport · операторы IS

- Куда можно уехать в плацкарте дешевле 9000 рублей?
  → FETCH [FARES] WHERE @price_rub BELOW 9000 && @fare_class IS 'platskart'
  # слот 248 · 2 условия · && · без суффикса · предмет назван · поля @price_rub @fare_class · операторы BELOW IS

- Списком нужны цены на проезд внутри Железноводска
  → FETCH [FARES] WHERE @route_end IS 'Железноводск' && @route_start IS 'Железноводск' AS LIST
  # слот 256 · 2 условия · && · AS LIST · предмет назван · поля @route_end @route_start · операторы IS

## Три условия

- Ищу поездку на трамвае за 20-40 рублей, покажи варианты.
  → FETCH [FARES] WHERE @transport IS 'tram' && @price_rub ABOVE 20 && @price_rub BELOW 40
  # слот 32 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @transport @price_rub · операторы IS ABOVE BELOW

- Выдай рейсы до Питера, Москвы и Сочи в json.
  → FETCH [FARES] WHERE @route_end IS 'Санкт-Петербург' || @route_end IS 'Москва' || @route_end IS 'Сочи' AS JSON
  # слот 43 · 3 условия · || · AS JSON · предмет назван · поля @route_end · операторы IS

- Нужны авиабилеты дороже 23000 рублей, но дешевле 25000 рублей — ответ в json.
  → FETCH [FARES] WHERE @transport IS 'plane' && @price_rub ABOVE 23000 && @price_rub BELOW 25000 AS JSON
  # слот 53 · 3 условия · && · AS JSON · диапазон · предмет назван · поля @transport @price_rub · операторы IS ABOVE BELOW

- Возьму купе — покажи цены выше 10000 рублей и ниже 12000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @price_rub ABOVE 10000 && @price_rub BELOW 12000
  # слот 54 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @fare_class @price_rub · операторы IS ABOVE BELOW

- Перечисли поезда из Москвы с купейными местами.
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @transport IS 'train' && @route_start IS 'Москва'
  # слот 64 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @transport @route_start · операторы IS

- Планирую кататься на трамвае внутри Пятигорска — покажи цены на проезд таблицей.
  → FETCH [FARES] WHERE @transport IS 'tram' && @route_start IS 'Пятигорск' && @route_end IS 'Пятигорск' AS TABLE
  # слот 71 · 3 условия · && · AS TABLE · предмет назван · поля @transport @route_start @route_end · операторы IS

- Покажи тарифы на поезд из Москвы в купе.
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @route_start IS 'Москва' && @transport IS 'train'
  # слот 104 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @route_start @transport · операторы IS

- Нужна таблица по плацкарту из Москвы, автобусы не подходят.
  → FETCH [FARES] WHERE @fare_class IS 'platskart' && @transport NOT 'bus' && @route_start IS 'Москва' AS TABLE
  # слот 111 · 3 условия · && · AS TABLE · предмет назван · поля @fare_class @transport @route_start · операторы IS NOT

- Собираюсь в Санкт-Петербург экономом — покажи билеты на самолёт.
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @transport IS 'plane' && @route_end IS 'Санкт-Петербург'
  # слот 146 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @transport @route_end · операторы IS

- Дай таблицей плацкарт до Пятигорска дешевле 8000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'platskart' && @price_rub BELOW 8000 && @route_end IS 'Пятигорск' AS TABLE
  # слот 147 · 3 условия · && · AS TABLE · предмет назван · поля @fare_class @price_rub @route_end · операторы IS BELOW

- Найди билеты бизнес-классом до Москвы дешевле 24000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'business' && @route_end IS 'Москва' && @price_rub BELOW 24000
  # слот 161 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @route_end @price_rub · операторы IS BELOW

- Собираюсь ехать в купе из Москвы — подбери варианты дешевле 11000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @price_rub BELOW 11000 && @route_start IS 'Москва'
  # слот 189 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @price_rub @route_start · операторы IS BELOW

- Уезжаю из Минеральных Вод в Новосибирск — покажи варианты дороже 14000 рублей.
  → FETCH [FARES] WHERE @route_end IS 'Новосибирск' && @price_rub ABOVE 14000 && @route_start IS 'Минеральные Воды'
  # слот 192 · 3 условия · && · без суффикса · предмет назван · поля @route_end @price_rub @route_start · операторы IS ABOVE

- Как доехать из Нальчика в Минеральные Воды дешевле 400 рублей? Ответ списком.
  → FETCH [FARES] WHERE @route_start IS 'Нальчик' && @route_end IS 'Минеральные Воды' && @price_rub BELOW 400 AS LIST
  # слот 196 · 3 условия · && · AS LIST · предмет назван · поля @route_start @route_end @price_rub · операторы IS BELOW

- Еду из Пятигорска в Нальчик, поищи билеты дешевле 300 рублей.
  → FETCH [FARES] WHERE @price_rub BELOW 300 && @route_end IS 'Нальчик' && @route_start IS 'Пятигорск'
  # слот 197 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @route_end @route_start · операторы BELOW IS

- Что ходит по Иноземцево дешевле 40 рублей?
  → FETCH [FARES] WHERE @route_end IS 'Иноземцево' && @route_start IS 'Иноземцево' && @price_rub BELOW 40
  # слот 249 · 3 условия · && · без суффикса · предмет назван · поля @route_end @route_start @price_rub · операторы IS BELOW

## Четыре условия

- Еду поездом в купе — перечисли билеты дороже 10000 рублей и дешевле 20000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @transport IS 'train' && @price_rub ABOVE 10000 && @price_rub BELOW 20000
  # слот 7 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @fare_class @transport @price_rub · операторы IS ABOVE BELOW

- Покажи тарифы эконом-класса на самолёт дороже 7000 рублей и дешевле 10000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @transport IS 'plane' && @price_rub ABOVE 7000 && @price_rub BELOW 10000
  # слот 37 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @fare_class @transport @price_rub · операторы IS ABOVE BELOW

- Собираюсь уехать из Кисловодска на автобусе: покажи рейсы дороже 30 рублей и дешевле 50 рублей.
  → FETCH [FARES] WHERE @transport IS 'bus' && @price_rub ABOVE 30 && @price_rub BELOW 50 && @route_start IS 'Кисловодск'
  # слот 41 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @transport @price_rub @route_start · операторы IS ABOVE BELOW

- Лечу из Минеральных Вод в Москву бизнес-классом — покажи цены на билеты.
  → FETCH [FARES] WHERE @fare_class IS 'business' && @transport IS 'plane' && @route_start IS 'Минеральные Воды' && @route_end IS 'Москва'
  # слот 95 · 4 условия · && · без суффикса · предмет назван · поля @fare_class @transport @route_start @route_end · операторы IS

- Списком покажи перелёты из Мин-Вод бизнес-классом дешевле 24000 рублей.
  → FETCH [FARES] WHERE @fare_class IS 'business' && @transport IS 'plane' && @route_start IS 'Минеральные Воды' && @price_rub BELOW 24000 AS LIST
  # слот 148 · 4 условия · && · AS LIST · предмет назван · поля @fare_class @transport @route_start @price_rub · операторы IS BELOW

- Какие трамвайные поездки по Пятигорску стоят дороже 20 рублей?
  → FETCH [FARES] WHERE @transport IS 'tram' && @route_start IS 'Пятигорск' && @price_rub ABOVE 20 && @route_end IS 'Пятигорск'
  # слот 149 · 4 условия · && · без суффикса · предмет назван · поля @transport @route_start @price_rub @route_end · операторы IS ABOVE

- Еду по Железноводску автобусом, покажи варианты дешевле 70 рублей
  → FETCH [FARES] WHERE @route_start IS 'Железноводск' && @price_rub BELOW 70 && @route_end IS 'Железноводск' && @transport IS 'bus'
  # слот 234 · 4 условия · && · без суффикса · предмет назван · поля @route_start @price_rub @route_end @transport · операторы IS BELOW

- Передвигаюсь внутри Кисловодска, за город не выезжаю — нужны в json тарифы дешевле 40 рублей, кроме самолёта.
  → FETCH [FARES] WHERE @route_end IS 'Кисловодск' && @route_start IS 'Кисловодск' && @price_rub BELOW 40 && @transport NOT 'plane' AS JSON
  # слот 241 · 4 условия · && · AS JSON · предмет назван · поля @route_end @route_start @price_rub @transport · операторы IS BELOW NOT
