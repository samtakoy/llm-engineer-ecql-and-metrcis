# FARES

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Что есть в бизнес-классе?
  → FETCH [FARES] WHERE @fare_class IS 'business'
  # слот 9 · одно условие · без связки · без суффикса · предмет назван · поля @fare_class · операторы IS

- Автобусы, json
  → FETCH [FARES] WHERE @transport IS 'bus' AS JSON
  # слот 58 · одно условие · без связки · AS JSON · предмет назван · поля @transport · операторы IS

- Что в экономе?
  → FETCH [FARES] WHERE @fare_class IS 'economy'
  # слот 80 · одно условие · без связки · без суффикса · предмет назван · поля @fare_class · операторы IS

- Плацкартные билеты
  → FETCH [FARES] WHERE @fare_class IS 'platskart'
  # слот 94 · одно условие · без связки · без суффикса · предмет назван · поля @fare_class · операторы IS

- Трамвайные тарифы сведи в таблицу
  → FETCH [FARES] WHERE @transport IS 'tram' AS TABLE
  # слот 141 · одно условие · без связки · AS TABLE · предмет назван · поля @transport · операторы IS

- Как добраться до Казани?
  → FETCH [FARES] WHERE @route_end IS 'Казань'
  # слот 190 · одно условие · без связки · без суффикса · предмет назван · поля @route_end · операторы IS

- Рейсы до Самары — дай json
  → FETCH [FARES] WHERE @route_end IS 'Самара' AS JSON
  # слот 219 · одно условие · без связки · AS JSON · предмет назван · поля @route_end · операторы IS

- Что отправляется из Санкт-Петербурга?
  → FETCH [FARES] WHERE @route_start IS 'Санкт-Петербург'
  # слот 229 · одно условие · без связки · без суффикса · предмет назван · поля @route_start · операторы IS

## Два условия

- Плацкарт на поезде
  → FETCH [FARES] WHERE @fare_class IS 'platskart' && @transport IS 'train'
  # слот 14 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @transport · операторы IS

- Автобусы дороже тридцати рублей
  → FETCH [FARES] WHERE @transport IS 'bus' && @price_rub ABOVE 30
  # слот 15 · 2 условия · && · без суффикса · предмет назван · поля @transport @price_rub · операторы IS ABOVE

- Эконом на самолёте
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @transport IS 'plane'
  # слот 59 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @transport · операторы IS

- Бизнес-класс на самолёте
  → FETCH [FARES] WHERE @fare_class IS 'business' && @transport IS 'plane'
  # слот 67 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @transport · операторы IS

- Автобусы до Кисловодска, покажи таблицей
  → FETCH [FARES] WHERE @transport IS 'bus' && @route_end IS 'Кисловодск' AS TABLE
  # слот 132 · 2 условия · && · AS TABLE · предмет назван · поля @transport @route_end · операторы IS

- Трамваи из Пятигорска, списком
  → FETCH [FARES] WHERE @transport IS 'tram' && @route_start IS 'Пятигорск' AS LIST
  # слот 145 · 2 условия · && · AS LIST · предмет назван · поля @transport @route_start · операторы IS

- Эконом из Минеральных Вод
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @route_start IS 'Минеральные Воды'
  # слот 152 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @route_start · операторы IS

- Бизнес дороже двадцати трёх тысяч
  → FETCH [FARES] WHERE @fare_class IS 'business' && @price_rub ABOVE 23000
  # слот 171 · 2 условия · && · без суффикса · предмет назван · поля @fare_class @price_rub · операторы IS ABOVE

- До Екатеринбурга дороже двадцати восьми тысяч
  → FETCH [FARES] WHERE @route_end IS 'Екатеринбург' && @price_rub ABOVE 28000
  # слот 195 · 2 условия · && · без суффикса · предмет назван · поля @route_end @price_rub · операторы IS ABOVE

- До Нижнего Новгорода дешевле двадцати семи тысяч — нужен список
  → FETCH [FARES] WHERE @price_rub BELOW 27000 && @route_end IS 'Нижний Новгород' AS LIST
  # слот 205 · 2 условия · && · AS LIST · предмет назван · поля @price_rub @route_end · операторы BELOW IS

- Самолётом или поездом
  → FETCH [FARES] WHERE @transport IS 'plane' || @transport IS 'train'
  # слот 209 · 2 условия · || · без суффикса · предмет назван · поля @transport · операторы IS

- Плацкарт дешевле девяти тысяч
  → FETCH [FARES] WHERE @price_rub BELOW 9000 && @fare_class IS 'platskart'
  # слот 248 · 2 условия · && · без суффикса · предмет назван · поля @price_rub @fare_class · операторы BELOW IS

- Проезд по Железноводску, просто назови списком
  → FETCH [FARES] WHERE @route_end IS 'Железноводск' && @route_start IS 'Железноводск' AS LIST
  # слот 256 · 2 условия · && · AS LIST · предмет назван · поля @route_end @route_start · операторы IS

## Три условия

- Трамвай за двадцать-сорок рублей
  → FETCH [FARES] WHERE @transport IS 'tram' && @price_rub ABOVE 20 && @price_rub BELOW 40
  # слот 32 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @transport @price_rub · операторы IS ABOVE BELOW

- Питер, Москва, Сочи — рейсы в json
  → FETCH [FARES] WHERE @route_end IS 'Санкт-Петербург' || @route_end IS 'Москва' || @route_end IS 'Сочи' AS JSON
  # слот 43 · 3 условия · || · AS JSON · предмет назван · поля @route_end · операторы IS

- Авиабилеты за двадцать три — двадцать пять тысяч, json
  → FETCH [FARES] WHERE @transport IS 'plane' && @price_rub ABOVE 23000 && @price_rub BELOW 25000 AS JSON
  # слот 53 · 3 условия · && · AS JSON · диапазон · предмет назван · поля @transport @price_rub · операторы IS ABOVE BELOW

- Купе от десяти до двенадцати тысяч
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @price_rub ABOVE 10000 && @price_rub BELOW 12000
  # слот 54 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @fare_class @price_rub · операторы IS ABOVE BELOW

- Купе поездом из Москвы
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @transport IS 'train' && @route_start IS 'Москва'
  # слот 64 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @transport @route_start · операторы IS

- Трамвай по Пятигорску — в таблицу
  → FETCH [FARES] WHERE @transport IS 'tram' && @route_start IS 'Пятигорск' && @route_end IS 'Пятигорск' AS TABLE
  # слот 71 · 3 условия · && · AS TABLE · предмет назван · поля @transport @route_start @route_end · операторы IS

- Поезд из Москвы, купе
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @route_start IS 'Москва' && @transport IS 'train'
  # слот 104 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @route_start @transport · операторы IS

- Плацкарт из Москвы, автобусы не считаем — сравни таблицей
  → FETCH [FARES] WHERE @fare_class IS 'platskart' && @transport NOT 'bus' && @route_start IS 'Москва' AS TABLE
  # слот 111 · 3 условия · && · AS TABLE · предмет назван · поля @fare_class @transport @route_start · операторы IS NOT

- Эконом до Санкт-Петербурга
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @transport IS 'plane' && @route_end IS 'Санкт-Петербург'
  # слот 146 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @transport @route_end · операторы IS

- Плацкарт до Пятигорска дешевле восьми тысяч, табличкой
  → FETCH [FARES] WHERE @fare_class IS 'platskart' && @price_rub BELOW 8000 && @route_end IS 'Пятигорск' AS TABLE
  # слот 147 · 3 условия · && · AS TABLE · предмет назван · поля @fare_class @price_rub @route_end · операторы IS BELOW

- Бизнес до Москвы дешевле двадцати четырёх тысяч
  → FETCH [FARES] WHERE @fare_class IS 'business' && @route_end IS 'Москва' && @price_rub BELOW 24000
  # слот 161 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @route_end @price_rub · операторы IS BELOW

- Купе из Москвы дешевле одиннадцати тысяч
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @price_rub BELOW 11000 && @route_start IS 'Москва'
  # слот 189 · 3 условия · && · без суффикса · предмет назван · поля @fare_class @price_rub @route_start · операторы IS BELOW

- Из Минвод в Новосибирск дороже четырнадцати тысяч
  → FETCH [FARES] WHERE @route_end IS 'Новосибирск' && @price_rub ABOVE 14000 && @route_start IS 'Минеральные Воды'
  # слот 192 · 3 условия · && · без суффикса · предмет назван · поля @route_end @price_rub @route_start · операторы IS ABOVE

- Из Нальчика в Минеральные Воды дешевле четырёхсот — как доехать, списком
  → FETCH [FARES] WHERE @route_start IS 'Нальчик' && @route_end IS 'Минеральные Воды' && @price_rub BELOW 400 AS LIST
  # слот 196 · 3 условия · && · AS LIST · предмет назван · поля @route_start @route_end @price_rub · операторы IS BELOW

- Из Пятигорска в Нальчик дешевле трёхсот
  → FETCH [FARES] WHERE @price_rub BELOW 300 && @route_end IS 'Нальчик' && @route_start IS 'Пятигорск'
  # слот 197 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @route_end @route_start · операторы BELOW IS

- Проезд по Иноземцево дешевле сорока рублей
  → FETCH [FARES] WHERE @route_end IS 'Иноземцево' && @route_start IS 'Иноземцево' && @price_rub BELOW 40
  # слот 249 · 3 условия · && · без суффикса · предмет назван · поля @route_end @route_start @price_rub · операторы IS BELOW

## Четыре условия

- Купе на поезде от десяти до двадцати тысяч
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @transport IS 'train' && @price_rub ABOVE 10000 && @price_rub BELOW 20000
  # слот 7 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @fare_class @transport @price_rub · операторы IS ABOVE BELOW

- Эконом на самолёт за семь-десять тысяч
  → FETCH [FARES] WHERE @fare_class IS 'economy' && @transport IS 'plane' && @price_rub ABOVE 7000 && @price_rub BELOW 10000
  # слот 37 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @fare_class @transport @price_rub · операторы IS ABOVE BELOW

- Автобус из Кисловодска за тридцать-пятьдесят рублей
  → FETCH [FARES] WHERE @transport IS 'bus' && @price_rub ABOVE 30 && @price_rub BELOW 50 && @route_start IS 'Кисловодск'
  # слот 41 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @transport @price_rub @route_start · операторы IS ABOVE BELOW

- Бизнес из Минвод в Москву
  → FETCH [FARES] WHERE @fare_class IS 'business' && @transport IS 'plane' && @route_start IS 'Минеральные Воды' && @route_end IS 'Москва'
  # слот 95 · 4 условия · && · без суффикса · предмет назван · поля @fare_class @transport @route_start @route_end · операторы IS

- Бизнес из Минеральных Вод дешевле двадцати четырёх тысяч, списком
  → FETCH [FARES] WHERE @fare_class IS 'business' && @transport IS 'plane' && @route_start IS 'Минеральные Воды' && @price_rub BELOW 24000 AS LIST
  # слот 148 · 4 условия · && · AS LIST · предмет назван · поля @fare_class @transport @route_start @price_rub · операторы IS BELOW

- Трамвай по Пятигорску дороже двадцати рублей
  → FETCH [FARES] WHERE @transport IS 'tram' && @route_start IS 'Пятигорск' && @price_rub ABOVE 20 && @route_end IS 'Пятигорск'
  # слот 149 · 4 условия · && · без суффикса · предмет назван · поля @transport @route_start @price_rub @route_end · операторы IS ABOVE

- Автобус по Железноводску дешевле семидесяти рублей
  → FETCH [FARES] WHERE @route_start IS 'Железноводск' && @price_rub BELOW 70 && @route_end IS 'Железноводск' && @transport IS 'bus'
  # слот 234 · 4 условия · && · без суффикса · предмет назван · поля @route_start @price_rub @route_end @transport · операторы IS BELOW

- Проезд по Кисловодску дешевле сорока рублей, без самолётов — json
  → FETCH [FARES] WHERE @route_end IS 'Кисловодск' && @route_start IS 'Кисловодск' && @price_rub BELOW 40 && @transport NOT 'plane' AS JSON
  # слот 241 · 4 условия · && · AS JSON · предмет назван · поля @route_end @route_start @price_rub @transport · операторы IS BELOW NOT
