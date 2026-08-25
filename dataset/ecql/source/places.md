# PLACES

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Интересуют вокзалы, автовокзалы и аэропорты — покажи списком.
  → FETCH [PLACES] WHERE @category IS 'transport' AS LIST
  # слот 21 · одно условие · без связки · AS LIST · предмет назван · поля @category · операторы IS

- Какие есть памятники?
  → FETCH [PLACES] WHERE @object_kind IS 'monument'
  # слот 47 · одно условие · без связки · без суффикса · предмет назван · поля @object_kind · операторы IS

- Найди терренкуры, станции маршрута и галереи.
  → FETCH [PLACES] WHERE @category IS 'service'
  # слот 50 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Развлечения нужны в json
  → FETCH [PLACES] WHERE @category IS 'activity' AS JSON
  # слот 56 · одно условие · без связки · AS JSON · предмет назван · поля @category · операторы IS

- Разомнусь в поездке: подскажи бассейны, спортзалы и стадионы.
  → FETCH [PLACES] WHERE @category IS 'activity'
  # слот 68 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Что относится к ансамблям?
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble'
  # слот 73 · одно условие · без связки · без суффикса · предмет назван · поля @object_kind · операторы IS

- Где поесть?
  → FETCH [PLACES] WHERE @category IS 'food'
  # слот 81 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Хочу пройтись по бюветам и родникам — дай их списком.
  → FETCH [PLACES] WHERE @category IS 'water' AS LIST
  # слот 96 · одно условие · без связки · AS LIST · предмет назван · поля @category · операторы IS

- Выведи таблицей парки, скверы и озёра.
  → FETCH [PLACES] WHERE @category IS 'nature' AS TABLE
  # слот 110 · одно условие · без связки · AS TABLE · предмет назван · поля @category · операторы IS

- Назови вокзалы, автовокзалы и аэропорты.
  → FETCH [PLACES] WHERE @category IS 'transport'
  # слот 114 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Планирую обойти достопримечательные места — дай их в json.
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' AS JSON
  # слот 120 · одно условие · без связки · AS JSON · предмет назван · поля @object_kind · операторы IS

- Что посмотреть из культурного?
  → FETCH [PLACES] WHERE @category IS 'culture'
  # слот 142 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Где остановиться?
  → FETCH [PLACES] WHERE @category IS 'lodging'
  # слот 155 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Что такое «Арго»?
  → FETCH [PLACES] WHERE @name IS 'Арго'
  # слот 214 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

- Что есть в Пятигорске?
  → FETCH [PLACES] WHERE @city IS 'Пятигорск'
  # слот 245 · одно условие · без связки · без суффикса · поля @city · операторы IS

- Где указан средний чек? Списком
  → FETCH [PLACES] WHERE @price_kind IS 'average_check' AS LIST
  # слот 247 · одно условие · без связки · AS LIST · предмет назван · поля @price_kind · операторы IS

## Два условия

- Какие родники числятся памятниками?
  → FETCH [PLACES] WHERE @category IS 'water' && @object_kind IS 'monument'
  # слот 1 · 2 условия · && · без суффикса · предмет назван · поля @category @object_kind · операторы IS

- Куда из развлечений с коляской не попасть?
  → FETCH [PLACES] WHERE @wheelchair IS 'no' && @category IS 'activity'
  # слот 2 · 2 условия · && · без суффикса · предмет назван · поля @wheelchair @category · операторы IS

- Хочу увидеть достопримечательные места под региональной охраной.
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' && @heritage_status IS 'regional'
  # слот 4 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status · операторы IS

- Покажи кафе и рестораны, куда с коляской не пускают.
  → FETCH [PLACES] WHERE @wheelchair IS 'no' && @category IS 'food'
  # слот 13 · 2 условия · && · без суффикса · предмет назван · поля @wheelchair @category · операторы IS

- Заведения со средним чеком и частичным доступом для колясок
  → FETCH [PLACES] WHERE @price_kind IS 'average_check' && @wheelchair IS 'limited'
  # слот 30 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @wheelchair · операторы IS

- В какие отели с коляской не попасть?
  → FETCH [PLACES] WHERE @category IS 'lodging' && @wheelchair IS 'no'
  # слот 36 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Перечисли памятники, куда можно заехать с коляской.
  → FETCH [PLACES] WHERE @object_kind IS 'monument' && @wheelchair IS 'yes'
  # слот 46 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @wheelchair · операторы IS

- В какие магазины можно попасть с коляской?
  → FETCH [PLACES] WHERE @category IS 'shopping' && @wheelchair IS 'yes'
  # слот 57 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Назови места с ценой за ночь, куда с коляской не попасть.
  → FETCH [PLACES] WHERE @price_kind IS 'per_night' && @wheelchair IS 'no'
  # слот 63 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @wheelchair · операторы IS

- Ищу памятники под региональной охраной.
  → FETCH [PLACES] WHERE @object_kind IS 'monument' && @heritage_status IS 'regional'
  # слот 70 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status · операторы IS

- Ищу ансамбли федеральной охраны.
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble' && @heritage_status IS 'federal'
  # слот 74 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status · операторы IS

- Найди в Пятигорске бассейны и спортзалы.
  → FETCH [PLACES] WHERE @category IS 'activity' && @city IS 'Пятигорск'
  # слот 79 · 2 условия · && · без суффикса · предмет назван · поля @category @city · операторы IS

- Культурные объекты без доступа для колясок
  → FETCH [PLACES] WHERE @category IS 'culture' && @wheelchair IS 'no'
  # слот 89 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Ищу ночлег с оплатой за ночь.
  → FETCH [PLACES] WHERE @price_kind IS 'per_night' && @category IS 'lodging'
  # слот 92 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @category · операторы IS

- Что есть в Ессентуках и Кисловодске?
  → FETCH [PLACES] WHERE @city IS 'Ессентуки' || @city IS 'Кисловодск'
  # слот 97 · 2 условия · || · без суффикса · поля @city · операторы IS

- Выгрузи в json памятники и музеи под региональной охраной.
  → FETCH [PLACES] WHERE @category IS 'culture' && @heritage_status IS 'regional' AS JSON
  # слот 99 · 2 условия · && · AS JSON · предмет назван · поля @category @heritage_status · операторы IS

- Отбери музеи и церкви, куда пускают с коляской.
  → FETCH [PLACES] WHERE @category IS 'culture' && @wheelchair IS 'yes'
  # слот 103 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Хочу посмотреть памятники под местной охраной.
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @object_kind IS 'monument'
  # слот 106 · 2 условия · && · без суффикса · предмет назван · поля @heritage_status @object_kind · операторы IS

- Интересуют бюветы под федеральной охраной.
  → FETCH [PLACES] WHERE @category IS 'water' && @heritage_status IS 'federal'
  # слот 119 · 2 условия · && · без суффикса · предмет назван · поля @category @heritage_status · операторы IS

- Подскажи, куда сходить: памятники, музеи и церкви под местной охраной.
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @category IS 'culture'
  # слот 122 · 2 условия · && · без суффикса · предмет назван · поля @heritage_status @category · операторы IS

- Покажи в json Особняк Тиц с местной охраной.
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @name IS 'Особняк Тиц' AS JSON
  # слот 151 · 2 условия · && · AS JSON · предмет назван · поля @heritage_status @name · операторы IS

- Подскажи ансамбли под федеральной охраной.
  → FETCH [PLACES] WHERE @heritage_status IS 'federal' && @object_kind IS 'ensemble'
  # слот 162 · 2 условия · && · без суффикса · предмет назван · поля @heritage_status @object_kind · операторы IS

- Что стоит дороже 11000 рублей за ночь?
  → FETCH [PLACES] WHERE @price_rub ABOVE 11000 && @price_kind IS 'per_night'
  # слот 179 · 2 условия · && · без суффикса · предмет назван · поля @price_rub @price_kind · операторы ABOVE IS

- Покажи «Plaza банкетный зал», если цена там ниже 2000 рублей.
  → FETCH [PLACES] WHERE @price_rub BELOW 2000 && @name IS 'Plaza банкетный зал'
  # слот 181 · 2 условия · && · без суффикса · предмет назван · поля @price_rub @name · операторы BELOW IS

- Покажи, что известно про «Лиану» в Лермонтове.
  → FETCH [PLACES] WHERE @city IS 'Лермонтов' && @name IS 'Лиана'
  # слот 182 · 2 условия · && · без суффикса · предмет назван · поля @city @name · операторы IS

- Перечисли кафе или парки, куда можно заглянуть.
  → FETCH [PLACES] WHERE @category IS 'food' || @category IS 'nature'
  # слот 183 · 2 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Куда сходить в Ессентуках или Пятигорске? Ответ списком.
  → FETCH [PLACES] WHERE @city IS 'Ессентуки' || @city IS 'Пятигорск' AS LIST
  # слот 207 · 2 условия · || · AS LIST · поля @city · операторы IS

- Глянь «Асторию», если там дешевле 400 рублей. Ответ надо в виде json.
  → FETCH [PLACES] WHERE @name IS 'Астория' && @price_rub BELOW 400 AS JSON
  # слот 211 · 2 условия · && · AS JSON · предмет назван · поля @name @price_rub · операторы IS BELOW

- Есть информация по Домашней церкови-часовни в Иноземцево?
  → FETCH [PLACES] WHERE @name IS 'Домашняя церковь-часовня' && @city IS 'Иноземцево'
  # слот 213 · 2 условия · && · без суффикса · предмет назван · поля @name @city · операторы IS

- «Гирос & Пицца» в Минеральных Водах — покажи табличкой
  → FETCH [PLACES] WHERE @name IS 'Гирос & Пицца' && @city IS 'Минеральные Воды' AS TABLE
  # слот 216 · 2 условия · && · AS TABLE · предмет назван · поля @name @city · операторы IS

- Присмотрел «Эос» — беру, если дешевле 6000 рублей - есть такой вариант?
  → FETCH [PLACES] WHERE @name IS 'Эос' && @price_rub BELOW 6000
  # слот 218 · 2 условия · && · без суффикса · предмет назван · поля @name @price_rub · операторы IS BELOW

- В «БутерBro» дешевле 400?
  → FETCH [PLACES] WHERE @name IS 'БутерBro' && @price_rub BELOW 400
  # слот 231 · 2 условия · && · без суффикса · предмет назван · поля @name @price_rub · операторы IS BELOW

- Готов отдать больше 200 рублей за визит, ночевать не собираюсь. Куда сходить?
  → FETCH [PLACES] WHERE @price_kind NOT 'per_night' && @price_rub ABOVE 200
  # слот 233 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @price_rub · операторы NOT ABOVE

- Покажи «Пространство лофт», если он дороже 4000 рублей
  → FETCH [PLACES] WHERE @name IS 'Пространство лофт' && @price_rub ABOVE 4000
  # слот 240 · 2 условия · && · без суффикса · предмет назван · поля @name @price_rub · операторы IS ABOVE

- Нужен «Почтамтъ», где доступ для колясок не частичный.
  → FETCH [PLACES] WHERE @name IS 'Почтамтъ' && @wheelchair NOT 'limited'
  # слот 254 · 2 условия · && · без суффикса · предмет назван · поля @name @wheelchair · операторы IS NOT

- Ищу кафе, ресторан или столовую дороже 200 рублей — куда сходить?
  → FETCH [PLACES] WHERE @category IS 'food' && @price_rub ABOVE 200
  # слот 257 · 2 условия · && · без суффикса · предмет назван · поля @category @price_rub · операторы IS ABOVE

## Три условия

- Подбери места дороже 200 рублей и дешевле 1200 рублей, где платят не за ночь.
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 1200 && @price_kind NOT 'per_night'
  # слот 3 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @price_kind · операторы ABOVE BELOW NOT

- Прикидываю бюджет: сведи в таблицу места со средним чеком выше 200 рублей и ниже 400 рублей.
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 400 && @price_kind IS 'average_check' AS TABLE
  # слот 8 · 3 условия · && · AS TABLE · диапазон · предмет назван · поля @price_rub @price_kind · операторы ABOVE BELOW IS

- Нужен отель или гостевой дом ценой от 6000 до 16000 рублей — куда заселиться?
  → FETCH [PLACES] WHERE @price_rub ABOVE 6000 && @price_rub BELOW 16000 && @category IS 'lodging'
  # слот 17 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @category · операторы ABOVE BELOW IS

- Подскажи места, где средний чек выше 200 рублей и ниже 400 рублей.
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 400 && @price_kind IS 'average_check'
  # слот 24 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @price_kind · операторы ABOVE BELOW IS

- Оформи таблицей места от 900 до 1200 рублей, куда пускают с коляской.
  → FETCH [PLACES] WHERE @price_rub ABOVE 900 && @price_rub BELOW 1200 && @wheelchair IS 'yes' AS TABLE
  # слот 26 · 3 условия · && · AS TABLE · диапазон · поля @price_rub @wheelchair · операторы ABOVE BELOW IS

- Выведи, где цена за ночь выше 8000 рублей и ниже 13000 рублей.
  → FETCH [PLACES] WHERE @price_kind IS 'per_night' && @price_rub ABOVE 8000 && @price_rub BELOW 13000
  # слот 35 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_kind @price_rub · операторы IS ABOVE BELOW

- Хочу «ГироДот» с ценой выше 200 рублей и ниже 1200 рублей — покажи таблицей.
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 1200 && @name IS 'ГироДот' AS TABLE
  # слот 51 · 3 условия · && · AS TABLE · диапазон · предмет назван · поля @price_rub @name · операторы ABOVE BELOW IS

- Ищу ночлег дороже 8000 рублей, но дешевле 10000 — что посоветуешь?
  → FETCH [PLACES] WHERE @category IS 'lodging' && @price_rub ABOVE 8000 && @price_rub BELOW 10000
  # слот 55 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @category @price_rub · операторы IS ABOVE BELOW

- Посоветуй кафе дороже 200 рублей, но дешевле 500 рублей.
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 500 && @category IS 'food'
  # слот 61 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @category · операторы ABOVE BELOW IS

- Хочу заглянуть в музей, пройтись по терренкуру или набрать воды из родника — подбери варианты.
  → FETCH [PLACES] WHERE @category IS 'culture' || @category IS 'service' || @category IS 'water'
  # слот 66 · 3 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Едем за город, покажи кафе и столовые, у которых указан средний чек.
  → FETCH [PLACES] WHERE @category IS 'food' && @price_kind IS 'average_check' && @city IS 'вне городов'
  # слот 75 · 3 условия · && · без суффикса · предмет назван · поля @category @price_kind @city · операторы IS

- Подскажи достопримечательные места под региональной охраной, но галереи и терренкуры не предлагай.
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' && @heritage_status IS 'regional' && @category NOT 'service'
  # слот 78 · 3 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status @category · операторы IS NOT

- Культура, магазины или природа
  → FETCH [PLACES] WHERE @category IS 'culture' || @category IS 'shopping' || @category IS 'nature'
  # слот 84 · 3 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Найди источники Железноводска, куда с коляской пускают частично.
  → FETCH [PLACES] WHERE @category IS 'water' && @wheelchair IS 'limited' && @city IS 'Железноводск'
  # слот 86 · 3 условия · && · без суффикса · предмет назван · поля @category @wheelchair @city · операторы IS

- Расскажи про терренкур «Второй дед» в Железноводске
  → FETCH [PLACES] WHERE @category IS 'service' && @name IS 'Второй дед' && @city IS 'Железноводск'
  # слот 108 · 3 условия · && · без суффикса · предмет назван · поля @category @name @city · операторы IS

- Собери таблицу по церковным ансамблям, что не под местной охраной.
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble' && @category IS 'culture' && @heritage_status NOT 'local' AS TABLE
  # слот 117 · 3 условия · && · AS TABLE · предмет назван · поля @object_kind @category @heritage_status · операторы IS NOT

- Куда сходить в Пятигорске, Железноводске или вне городов?
  → FETCH [PLACES] WHERE @city IS 'Пятигорск' || @city IS 'вне городов' || @city IS 'Железноводск'
  # слот 128 · 3 условия · || · без суффикса · поля @city · операторы IS

- Что посмотреть в Мин-Водах, Кисловодске или Пятигорске?
  → FETCH [PLACES] WHERE @city IS 'Минеральные Воды' || @city IS 'Кисловодск' || @city IS 'Пятигорск'
  # слот 137 · 3 условия · || · без суффикса · поля @city · операторы IS

- Найди в Пятигорске парк или сквер — Сквер им. Анджиевского.
  → FETCH [PLACES] WHERE @category IS 'nature' && @name IS 'Сквер им. Анджиевского' && @city IS 'Пятигорск'
  # слот 154 · 3 условия · && · без суффикса · предмет назван · поля @category @name @city · операторы IS

- Интересует Особняк Тиц с местной охраной, и чтобы не ансамбль.
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @name IS 'Особняк Тиц' && @object_kind NOT 'ensemble'
  # слот 163 · 3 условия · && · без суффикса · предмет назван · поля @heritage_status @name @object_kind · операторы IS NOT

- Интересует станция маршрута «Ст. 4, терренкур 2» в Кисловодске — покажи её.
  → FETCH [PLACES] WHERE @category IS 'service' && @name IS 'Ст. 4, терренкур 2' && @city IS 'Кисловодск'
  # слот 169 · 3 условия · && · без суффикса · предмет назван · поля @category @name @city · операторы IS

- Ищу Съёмную квартиру в Кисловодске дороже 4000 рублей, покажи списком.
  → FETCH [PLACES] WHERE @price_rub ABOVE 4000 && @name IS 'Съёмная квартира' && @city IS 'Кисловодск' AS LIST
  # слот 177 · 3 условия · && · AS LIST · предмет назван · поля @price_rub @name @city · операторы ABOVE IS

- Подскажи места в Минеральных Водах со средним чеком ниже 1500 рублей.
  → FETCH [PLACES] WHERE @price_rub BELOW 1500 && @city IS 'Минеральные Воды' && @price_kind IS 'average_check'
  # слот 180 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @city @price_kind · операторы BELOW IS

- Дай таблицу по «Nefertiti» в Ессентуках дешевле 600 рублей.
  → FETCH [PLACES] WHERE @price_rub BELOW 600 && @name IS 'Nefertiti' && @city IS 'Ессентуки' AS TABLE
  # слот 184 · 3 условия · && · AS TABLE · предмет назван · поля @price_rub @name @city · операторы BELOW IS

- Дай списком отели, супермаркеты и вокзалы.
  → FETCH [PLACES] WHERE @category IS 'lodging' || @category IS 'shopping' || @category IS 'transport' AS LIST
  # слот 193 · 3 условия · || · AS LIST · предмет назван · поля @category · операторы IS

- Подбери в Ессентуках места дешевле 12000 рублей, средний чек исключи.
  → FETCH [PLACES] WHERE @price_rub BELOW 12000 && @city IS 'Ессентуки' && @price_kind NOT 'average_check'
  # слот 198 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @city @price_kind · операторы BELOW IS NOT

- Таблицей покажи, что есть в Мин-Водах, Кисловодске и Железноводске.
  → FETCH [PLACES] WHERE @city IS 'Минеральные Воды' || @city IS 'Кисловодск' || @city IS 'Железноводск' AS TABLE
  # слот 206 · 3 условия · || · AS TABLE · поля @city · операторы IS

- Покажи «Затерянный рай у Машука», если цена ниже 7000 рублей и с коляской там не отказывают.
  → FETCH [PLACES] WHERE @name IS 'Затерянный рай у Машука' && @price_rub BELOW 7000 && @wheelchair NOT 'no'
  # слот 208 · 3 условия · && · без суффикса · предмет назван · поля @name @price_rub @wheelchair · операторы IS BELOW NOT

- Где переночевать вне городов дешевле 5000 рублей за ночь?
  → FETCH [PLACES] WHERE @price_rub BELOW 5000 && @city IS 'вне городов' && @price_kind IS 'per_night'
  # слот 215 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @city @price_kind · операторы BELOW IS

- Что в Кисловодске идёт со средним чеком выше 200 рублей?
  → FETCH [PLACES] WHERE @price_kind IS 'average_check' && @price_rub ABOVE 200 && @city IS 'Кисловодск'
  # слот 230 · 3 условия · && · без суффикса · предмет назван · поля @price_kind @price_rub @city · операторы IS ABOVE

## Четыре условия

- Подбираю варианты дороже 1200 рублей и дешевле 2200 рублей, ночлег мне не нужен и полного доступа с коляской там быть не должно.
  → FETCH [PLACES] WHERE @price_rub ABOVE 1200 && @price_rub BELOW 2200 && @wheelchair NOT 'yes' && @category NOT 'lodging'
  # слот 11 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @wheelchair @category · операторы ABOVE BELOW NOT

- Покажи кафе «Смак» за городом с его средним чеком
  → FETCH [PLACES] WHERE @category IS 'food' && @price_kind IS 'average_check' && @name IS 'Смак' && @city IS 'вне городов'
  # слот 76 · 4 условия · && · без суффикса · предмет назван · поля @category @price_kind @name @city · операторы IS

- Интересует достопримечательное место «Исторический центр города Пятигорска» — памятники и музеи там, а охрана не федеральная.
  → FETCH [PLACES] WHERE @category IS 'culture' && @object_kind IS 'heritage_site' && @heritage_status NOT 'federal' && @name IS 'Исторический центр города Пятигорска'
  # слот 82 · 4 условия · && · без суффикса · предмет назван · поля @category @object_kind @heritage_status @name · операторы IS NOT

- Дай в json достопримечательное место «Исторический центр города Пятигорска» под региональной охраной, природу не бери.
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' && @heritage_status IS 'regional' && @name IS 'Исторический центр города Пятигорска' && @category NOT 'nature' AS JSON
  # слот 101 · 4 условия · && · AS JSON · предмет назван · поля @object_kind @heritage_status @name @category · операторы IS NOT

- Выведи кафе «Шалаши» с частичным доступом, где цена не за ночь.
  → FETCH [PLACES] WHERE @category IS 'food' && @wheelchair IS 'limited' && @name IS 'Шалаши' && @price_kind NOT 'per_night'
  # слот 102 · 4 условия · && · без суффикса · предмет назван · поля @category @wheelchair @name @price_kind · операторы IS NOT

- Интересуют ансамбли федеральной охраны в Железноводске, вокзалы и аэропорты пропусти.
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble' && @heritage_status IS 'federal' && @category NOT 'transport' && @city IS 'Железноводск'
  # слот 134 · 4 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status @category @city · операторы IS NOT

- Еда, культура, развлечения или магазины
  → FETCH [PLACES] WHERE @category IS 'food' || @category IS 'culture' || @category IS 'activity' || @category IS 'shopping'
  # слот 150 · 4 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Ищу «Шалаши» с частичным доступом и средним чеком ниже 1300 рублей.
  → FETCH [PLACES] WHERE @wheelchair IS 'limited' && @price_kind IS 'average_check' && @price_rub BELOW 1300 && @name IS 'Шалаши'
  # слот 173 · 4 условия · && · без суффикса · предмет назван · поля @wheelchair @price_kind @price_rub @name · операторы IS BELOW

- По Мин-Водам подойдёт что-то дешевле 7000 рублей, не магазин и средний чек ни при чём.
  → FETCH [PLACES] WHERE @price_rub BELOW 7000 && @city IS 'Минеральные Воды' && @category NOT 'shopping' && @price_kind NOT 'average_check'
  # слот 199 · 4 условия · && · без суффикса · предмет назван · поля @price_rub @city @category @price_kind · операторы BELOW IS NOT

- Таблицей выведи «Трактиръ На бульваре» в Кисловодске дешевле 400 рублей, плата там не за ночь.
  → FETCH [PLACES] WHERE @name IS 'Трактиръ На бульваре' && @price_rub BELOW 400 && @city IS 'Кисловодск' && @price_kind NOT 'per_night' AS TABLE
  # слот 202 · 4 условия · && · AS TABLE · предмет назван · поля @name @price_rub @city @price_kind · операторы IS BELOW NOT

- Нашёл «На двоих» в Ессентуках: беру при цене ниже 400 рублей, парки и озёра не подходят.
  → FETCH [PLACES] WHERE @name IS 'На двоих' && @city IS 'Ессентуки' && @price_rub BELOW 400 && @category NOT 'nature'
  # слот 204 · 4 условия · && · без суффикса · предмет назван · поля @name @city @price_rub @category · операторы IS BELOW NOT

- Нужен ночлег «Корона» дешевле 9000 рублей, и дело не в среднем чеке — таблицей.
  → FETCH [PLACES] WHERE @name IS 'Корона' && @price_rub BELOW 9000 && @category IS 'lodging' && @price_kind NOT 'average_check' AS TABLE
  # слот 227 · 4 условия · && · AS TABLE · предмет назван · поля @name @price_rub @category @price_kind · операторы IS BELOW NOT

- Хочу поужинать в кафе «Мангал» — покажи его, если средний чек выше 200 рублей.
  → FETCH [PLACES] WHERE @name IS 'Мангал' && @category IS 'food' && @price_kind IS 'average_check' && @price_rub ABOVE 200
  # слот 259 · 4 условия · && · без суффикса · предмет назван · поля @name @category @price_kind @price_rub · операторы IS ABOVE
