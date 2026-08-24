# PLACES

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Транспортные объекты — просто назови списком
  → FETCH [PLACES] WHERE @category IS 'transport' AS LIST
  # слот 21 · одно условие · без связки · AS LIST · предмет назван · поля @category · операторы IS

- Какие есть памятники?
  → FETCH [PLACES] WHERE @object_kind IS 'monument'
  # слот 47 · одно условие · без связки · без суффикса · предмет назван · поля @object_kind · операторы IS

- Какие тут бытовые услуги?
  → FETCH [PLACES] WHERE @category IS 'service'
  # слот 50 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Развлечения нужны в json
  → FETCH [PLACES] WHERE @category IS 'activity' AS JSON
  # слот 56 · одно условие · без связки · AS JSON · предмет назван · поля @category · операторы IS

- Чем заняться?
  → FETCH [PLACES] WHERE @category IS 'activity'
  # слот 68 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Что относится к ансамблям?
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble'
  # слот 73 · одно условие · без связки · без суффикса · предмет назван · поля @object_kind · операторы IS

- Где поесть?
  → FETCH [PLACES] WHERE @category IS 'food'
  # слот 81 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Источники, одним списком
  → FETCH [PLACES] WHERE @category IS 'water' AS LIST
  # слот 96 · одно условие · без связки · AS LIST · предмет назван · поля @category · операторы IS

- Природные объекты сведи в таблицу
  → FETCH [PLACES] WHERE @category IS 'nature' AS TABLE
  # слот 110 · одно условие · без связки · AS TABLE · предмет назван · поля @category · операторы IS

- Что относится к транспорту?
  → FETCH [PLACES] WHERE @category IS 'transport'
  # слот 114 · одно условие · без связки · без суффикса · предмет назван · поля @category · операторы IS

- Достопримечательные места — дай json
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

- Источники, которые считаются памятниками
  → FETCH [PLACES] WHERE @category IS 'water' && @object_kind IS 'monument'
  # слот 1 · 2 условия · && · без суффикса · предмет назван · поля @category @object_kind · операторы IS

- Развлечения без доступа для колясок
  → FETCH [PLACES] WHERE @wheelchair IS 'no' && @category IS 'activity'
  # слот 2 · 2 условия · && · без суффикса · предмет назван · поля @wheelchair @category · операторы IS

- Достопримечательные места регионального значения
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' && @heritage_status IS 'regional'
  # слот 4 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status · операторы IS

- Кафе, куда с коляской не заехать
  → FETCH [PLACES] WHERE @wheelchair IS 'no' && @category IS 'food'
  # слот 13 · 2 условия · && · без суффикса · предмет назван · поля @wheelchair @category · операторы IS

- Заведения со средним чеком и частичным доступом для колясок
  → FETCH [PLACES] WHERE @price_kind IS 'average_check' && @wheelchair IS 'limited'
  # слот 30 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @wheelchair · операторы IS

- Гостиницы без доступа для колясок
  → FETCH [PLACES] WHERE @category IS 'lodging' && @wheelchair IS 'no'
  # слот 36 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Памятники, куда можно подъехать на коляске
  → FETCH [PLACES] WHERE @object_kind IS 'monument' && @wheelchair IS 'yes'
  # слот 46 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @wheelchair · операторы IS

- Магазины с доступом для колясок
  → FETCH [PLACES] WHERE @category IS 'shopping' && @wheelchair IS 'yes'
  # слот 57 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Ночлег без доступа для колясок
  → FETCH [PLACES] WHERE @price_kind IS 'per_night' && @wheelchair IS 'no'
  # слот 63 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @wheelchair · операторы IS

- Памятники регионального значения
  → FETCH [PLACES] WHERE @object_kind IS 'monument' && @heritage_status IS 'regional'
  # слот 70 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status · операторы IS

- Ансамбли федерального значения
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble' && @heritage_status IS 'federal'
  # слот 74 · 2 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status · операторы IS

- Чем заняться в Пятигорске?
  → FETCH [PLACES] WHERE @category IS 'activity' && @city IS 'Пятигорск'
  # слот 79 · 2 условия · && · без суффикса · предмет назван · поля @category @city · операторы IS

- Культурные объекты без доступа для колясок
  → FETCH [PLACES] WHERE @category IS 'culture' && @wheelchair IS 'no'
  # слот 89 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Жильё, где цена указана за ночь
  → FETCH [PLACES] WHERE @price_kind IS 'per_night' && @category IS 'lodging'
  # слот 92 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @category · операторы IS

- Что есть в Ессентуках и Кисловодске?
  → FETCH [PLACES] WHERE @city IS 'Ессентуки' || @city IS 'Кисловодск'
  # слот 97 · 2 условия · || · без суффикса · поля @city · операторы IS

- Культурные объекты регионального значения, выгрузи json
  → FETCH [PLACES] WHERE @category IS 'culture' && @heritage_status IS 'regional' AS JSON
  # слот 99 · 2 условия · && · AS JSON · предмет назван · поля @category @heritage_status · операторы IS

- Культурные объекты с доступом для колясок
  → FETCH [PLACES] WHERE @category IS 'culture' && @wheelchair IS 'yes'
  # слот 103 · 2 условия · && · без суффикса · предмет назван · поля @category @wheelchair · операторы IS

- Памятники местного значения
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @object_kind IS 'monument'
  # слот 106 · 2 условия · && · без суффикса · предмет назван · поля @heritage_status @object_kind · операторы IS

- Источники федерального значения
  → FETCH [PLACES] WHERE @category IS 'water' && @heritage_status IS 'federal'
  # слот 119 · 2 условия · && · без суффикса · предмет назван · поля @category @heritage_status · операторы IS

- Культурные объекты под местной охраной
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @category IS 'culture'
  # слот 122 · 2 условия · && · без суффикса · предмет назван · поля @heritage_status @category · операторы IS

- Особняк Тиц, объект местного значения — нужен json
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @name IS 'Особняк Тиц' AS JSON
  # слот 151 · 2 условия · && · AS JSON · предмет назван · поля @heritage_status @name · операторы IS

- Ансамбли, охраняемые федерально
  → FETCH [PLACES] WHERE @heritage_status IS 'federal' && @object_kind IS 'ensemble'
  # слот 162 · 2 условия · && · без суффикса · предмет назван · поля @heritage_status @object_kind · операторы IS

- Ночь дороже одиннадцати тысяч
  → FETCH [PLACES] WHERE @price_rub ABOVE 11000 && @price_kind IS 'per_night'
  # слот 179 · 2 условия · && · без суффикса · предмет назван · поля @price_rub @price_kind · операторы ABOVE IS

- «Plaza банкетный зал» — уложусь в две тысячи?
  → FETCH [PLACES] WHERE @price_rub BELOW 2000 && @name IS 'Plaza банкетный зал'
  # слот 181 · 2 условия · && · без суффикса · предмет назван · поля @price_rub @name · операторы BELOW IS

- Что за «Лиана» в Лермонтове?
  → FETCH [PLACES] WHERE @city IS 'Лермонтов' && @name IS 'Лиана'
  # слот 182 · 2 условия · && · без суффикса · предмет назван · поля @city @name · операторы IS

- Еда или природа
  → FETCH [PLACES] WHERE @category IS 'food' || @category IS 'nature'
  # слот 183 · 2 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Ессентуки и Пятигорск, давай списком
  → FETCH [PLACES] WHERE @city IS 'Ессентуки' || @city IS 'Пятигорск' AS LIST
  # слот 207 · 2 условия · || · AS LIST · поля @city · операторы IS

- «Астория» дешевле четырёхсот, json
  → FETCH [PLACES] WHERE @name IS 'Астория' && @price_rub BELOW 400 AS JSON
  # слот 211 · 2 условия · && · AS JSON · предмет назван · поля @name @price_rub · операторы IS BELOW

- Домашняя церковь-часовня в Иноземцево
  → FETCH [PLACES] WHERE @name IS 'Домашняя церковь-часовня' && @city IS 'Иноземцево'
  # слот 213 · 2 условия · && · без суффикса · предмет назван · поля @name @city · операторы IS

- «Гирос & Пицца» в Минеральных Водах — покажи табличкой
  → FETCH [PLACES] WHERE @name IS 'Гирос & Пицца' && @city IS 'Минеральные Воды' AS TABLE
  # слот 216 · 2 условия · && · AS TABLE · предмет назван · поля @name @city · операторы IS

- «Эос» дешевле шести тысяч?
  → FETCH [PLACES] WHERE @name IS 'Эос' && @price_rub BELOW 6000
  # слот 218 · 2 условия · && · без суффикса · предмет назван · поля @name @price_rub · операторы IS BELOW

- «БутерBro» дешевле четырёхсот?
  → FETCH [PLACES] WHERE @name IS 'БутерBro' && @price_rub BELOW 400
  # слот 231 · 2 условия · && · без суффикса · предмет назван · поля @name @price_rub · операторы IS BELOW

- Дороже двухсот, но это не цена за ночь
  → FETCH [PLACES] WHERE @price_kind NOT 'per_night' && @price_rub ABOVE 200
  # слот 233 · 2 условия · && · без суффикса · предмет назван · поля @price_kind @price_rub · операторы NOT ABOVE

- «Пространство лофт» дороже четырёх тысяч?
  → FETCH [PLACES] WHERE @name IS 'Пространство лофт' && @price_rub ABOVE 4000
  # слот 240 · 2 условия · && · без суффикса · предмет назван · поля @name @price_rub · операторы IS ABOVE

- «Почтамтъ» — доступ для колясок там не частичный?
  → FETCH [PLACES] WHERE @name IS 'Почтамтъ' && @wheelchair NOT 'limited'
  # слот 254 · 2 условия · && · без суффикса · предмет назван · поля @name @wheelchair · операторы IS NOT

- Кафе дороже двухсот
  → FETCH [PLACES] WHERE @category IS 'food' && @price_rub ABOVE 200
  # слот 257 · 2 условия · && · без суффикса · предмет назван · поля @category @price_rub · операторы IS ABOVE

## Три условия

- От двухсот до тысячи двухсот, и это не цена за ночь
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 1200 && @price_kind NOT 'per_night'
  # слот 3 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @price_kind · операторы ABOVE BELOW NOT

- Средний чек от двухсот до четырёхсот, сведи в таблицу
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 400 && @price_kind IS 'average_check' AS TABLE
  # слот 8 · 3 условия · && · AS TABLE · диапазон · предмет назван · поля @price_rub @price_kind · операторы ABOVE BELOW IS

- Жильё от шести до шестнадцати тысяч
  → FETCH [PLACES] WHERE @price_rub ABOVE 6000 && @price_rub BELOW 16000 && @category IS 'lodging'
  # слот 17 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @category · операторы ABOVE BELOW IS

- Где средний чек от двухсот до четырёхсот?
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 400 && @price_kind IS 'average_check'
  # слот 24 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @price_kind · операторы ABOVE BELOW IS

- От девятисот до тысячи двухсот, с доступом для колясок — таблицей
  → FETCH [PLACES] WHERE @price_rub ABOVE 900 && @price_rub BELOW 1200 && @wheelchair IS 'yes' AS TABLE
  # слот 26 · 3 условия · && · AS TABLE · диапазон · поля @price_rub @wheelchair · операторы ABOVE BELOW IS

- Ночь от восьми до тринадцати тысяч
  → FETCH [PLACES] WHERE @price_kind IS 'per_night' && @price_rub ABOVE 8000 && @price_rub BELOW 13000
  # слот 35 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_kind @price_rub · операторы IS ABOVE BELOW

- «ГироДот» от двухсот до тысячи двухсот, в таблицу
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 1200 && @name IS 'ГироДот' AS TABLE
  # слот 51 · 3 условия · && · AS TABLE · диапазон · предмет назван · поля @price_rub @name · операторы ABOVE BELOW IS

- Жильё за восемь-десять тысяч
  → FETCH [PLACES] WHERE @category IS 'lodging' && @price_rub ABOVE 8000 && @price_rub BELOW 10000
  # слот 55 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @category @price_rub · операторы IS ABOVE BELOW

- Кафе от двухсот до пятисот
  → FETCH [PLACES] WHERE @price_rub ABOVE 200 && @price_rub BELOW 500 && @category IS 'food'
  # слот 61 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @category · операторы ABOVE BELOW IS

- Культура, услуги или источники
  → FETCH [PLACES] WHERE @category IS 'culture' || @category IS 'service' || @category IS 'water'
  # слот 66 · 3 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Кафе за городом, где указан средний чек
  → FETCH [PLACES] WHERE @category IS 'food' && @price_kind IS 'average_check' && @city IS 'вне городов'
  # слот 75 · 3 условия · && · без суффикса · предмет назван · поля @category @price_kind @city · операторы IS

- Достопримечательные места регионального значения, услуги не считаем
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' && @heritage_status IS 'regional' && @category NOT 'service'
  # слот 78 · 3 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status @category · операторы IS NOT

- Культура, магазины или природа
  → FETCH [PLACES] WHERE @category IS 'culture' || @category IS 'shopping' || @category IS 'nature'
  # слот 84 · 3 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- Источники Железноводска с частичным доступом для колясок
  → FETCH [PLACES] WHERE @category IS 'water' && @wheelchair IS 'limited' && @city IS 'Железноводск'
  # слот 86 · 3 условия · && · без суффикса · предмет назван · поля @category @wheelchair @city · операторы IS

- Что за «Второй дед» в Железноводске?
  → FETCH [PLACES] WHERE @category IS 'service' && @name IS 'Второй дед' && @city IS 'Железноводск'
  # слот 108 · 3 условия · && · без суффикса · предмет назван · поля @category @name @city · операторы IS

- Культурные ансамбли, кроме местного значения — сравни в таблице
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble' && @category IS 'culture' && @heritage_status NOT 'local' AS TABLE
  # слот 117 · 3 условия · && · AS TABLE · предмет назван · поля @object_kind @category @heritage_status · операторы IS NOT

- Пятигорск, Железноводск или что-нибудь за городом
  → FETCH [PLACES] WHERE @city IS 'Пятигорск' || @city IS 'вне городов' || @city IS 'Железноводск'
  # слот 128 · 3 условия · || · без суффикса · поля @city · операторы IS

- Минеральные Воды, Кисловодск или Пятигорск
  → FETCH [PLACES] WHERE @city IS 'Минеральные Воды' || @city IS 'Кисловодск' || @city IS 'Пятигорск'
  # слот 137 · 3 условия · || · без суффикса · поля @city · операторы IS

- Сквер имени Анджиевского в Пятигорске — это природа?
  → FETCH [PLACES] WHERE @category IS 'nature' && @name IS 'Сквер им. Анджиевского' && @city IS 'Пятигорск'
  # слот 154 · 3 условия · && · без суффикса · предмет назван · поля @category @name @city · операторы IS

- Особняк Тиц — местное значение, и это не ансамбль?
  → FETCH [PLACES] WHERE @heritage_status IS 'local' && @name IS 'Особняк Тиц' && @object_kind NOT 'ensemble'
  # слот 163 · 3 условия · && · без суффикса · предмет назван · поля @heritage_status @name @object_kind · операторы IS NOT

- Что за «Ст. 4, терренкур 2» в Кисловодске?
  → FETCH [PLACES] WHERE @category IS 'service' && @name IS 'Ст. 4, терренкур 2' && @city IS 'Кисловодск'
  # слот 169 · 3 условия · && · без суффикса · предмет назван · поля @category @name @city · операторы IS

- Съёмная квартира в Кисловодске дороже четырёх тысяч, распиши списком
  → FETCH [PLACES] WHERE @price_rub ABOVE 4000 && @name IS 'Съёмная квартира' && @city IS 'Кисловодск' AS LIST
  # слот 177 · 3 условия · && · AS LIST · предмет назван · поля @price_rub @name @city · операторы ABOVE IS

- Средний чек в Минводах меньше полутора тысяч
  → FETCH [PLACES] WHERE @price_rub BELOW 1500 && @city IS 'Минеральные Воды' && @price_kind IS 'average_check'
  # слот 180 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @city @price_kind · операторы BELOW IS

- «Nefertiti» в Ессентуках дешевле шестисот — в таблицу
  → FETCH [PLACES] WHERE @price_rub BELOW 600 && @name IS 'Nefertiti' && @city IS 'Ессентуки' AS TABLE
  # слот 184 · 3 условия · && · AS TABLE · предмет назван · поля @price_rub @name @city · операторы BELOW IS

- Жильё, магазины и транспорт — списком
  → FETCH [PLACES] WHERE @category IS 'lodging' || @category IS 'shopping' || @category IS 'transport' AS LIST
  # слот 193 · 3 условия · || · AS LIST · предмет назван · поля @category · операторы IS

- Ессентуки дешевле двенадцати тысяч, средний чек не нужен
  → FETCH [PLACES] WHERE @price_rub BELOW 12000 && @city IS 'Ессентуки' && @price_kind NOT 'average_check'
  # слот 198 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @city @price_kind · операторы BELOW IS NOT

- Минеральные Воды, Кисловодск, Железноводск — сравнить бы таблицей
  → FETCH [PLACES] WHERE @city IS 'Минеральные Воды' || @city IS 'Кисловодск' || @city IS 'Железноводск' AS TABLE
  # слот 206 · 3 условия · || · AS TABLE · поля @city · операторы IS

- «Затерянный рай у Машука» дешевле семи тысяч, и туда можно с коляской
  → FETCH [PLACES] WHERE @name IS 'Затерянный рай у Машука' && @price_rub BELOW 7000 && @wheelchair NOT 'no'
  # слот 208 · 3 условия · && · без суффикса · предмет назван · поля @name @price_rub @wheelchair · операторы IS BELOW NOT

- Ночь за городом дешевле пяти тысяч
  → FETCH [PLACES] WHERE @price_rub BELOW 5000 && @city IS 'вне городов' && @price_kind IS 'per_night'
  # слот 215 · 3 условия · && · без суффикса · предмет назван · поля @price_rub @city @price_kind · операторы BELOW IS

- Средний чек в Кисловодске выше двухсот
  → FETCH [PLACES] WHERE @price_kind IS 'average_check' && @price_rub ABOVE 200 && @city IS 'Кисловодск'
  # слот 230 · 3 условия · && · без суффикса · предмет назван · поля @price_kind @price_rub @city · операторы IS ABOVE

## Четыре условия

- От тысячи двухсот до двух тысяч двухсот, жильё не нужно и полного доступа для колясок нет
  → FETCH [PLACES] WHERE @price_rub ABOVE 1200 && @price_rub BELOW 2200 && @wheelchair NOT 'yes' && @category NOT 'lodging'
  # слот 11 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @price_rub @wheelchair @category · операторы ABOVE BELOW NOT

- «Смак» за городом — какой там средний чек?
  → FETCH [PLACES] WHERE @category IS 'food' && @price_kind IS 'average_check' && @name IS 'Смак' && @city IS 'вне городов'
  # слот 76 · 4 условия · && · без суффикса · предмет назван · поля @category @price_kind @name @city · операторы IS

- Исторический центр Пятигорска — он не федерального значения?
  → FETCH [PLACES] WHERE @category IS 'culture' && @object_kind IS 'heritage_site' && @heritage_status NOT 'federal' && @name IS 'Исторический центр города Пятигорска'
  # слот 82 · 4 условия · && · без суффикса · предмет назван · поля @category @object_kind @heritage_status @name · операторы IS NOT

- Исторический центр Пятигорска, не природа — json
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site' && @heritage_status IS 'regional' && @name IS 'Исторический центр города Пятигорска' && @category NOT 'nature' AS JSON
  # слот 101 · 4 условия · && · AS JSON · предмет назван · поля @object_kind @heritage_status @name @category · операторы IS NOT

- «Шалаши» — кафе с частичным доступом, и цена там не за ночь?
  → FETCH [PLACES] WHERE @category IS 'food' && @wheelchair IS 'limited' && @name IS 'Шалаши' && @price_kind NOT 'per_night'
  # слот 102 · 4 условия · && · без суффикса · предмет назван · поля @category @wheelchair @name @price_kind · операторы IS NOT

- Ансамбли федерального значения в Железноводске, транспорт не считаем
  → FETCH [PLACES] WHERE @object_kind IS 'ensemble' && @heritage_status IS 'federal' && @category NOT 'transport' && @city IS 'Железноводск'
  # слот 134 · 4 условия · && · без суффикса · предмет назван · поля @object_kind @heritage_status @category @city · операторы IS NOT

- Еда, культура, развлечения или магазины
  → FETCH [PLACES] WHERE @category IS 'food' || @category IS 'culture' || @category IS 'activity' || @category IS 'shopping'
  # слот 150 · 4 условия · || · без суффикса · предмет назван · поля @category · операторы IS

- «Шалаши»: средний чек меньше тысячи трёхсот, доступ частичный
  → FETCH [PLACES] WHERE @wheelchair IS 'limited' && @price_kind IS 'average_check' && @price_rub BELOW 1300 && @name IS 'Шалаши'
  # слот 173 · 4 условия · && · без суффикса · предмет назван · поля @wheelchair @price_kind @price_rub @name · операторы IS BELOW

- Минеральные Воды дешевле семи тысяч, без магазинов и без среднего чека
  → FETCH [PLACES] WHERE @price_rub BELOW 7000 && @city IS 'Минеральные Воды' && @category NOT 'shopping' && @price_kind NOT 'average_check'
  # слот 199 · 4 условия · && · без суффикса · предмет назван · поля @price_rub @city @category @price_kind · операторы BELOW IS NOT

- «Трактиръ На бульваре» в Кисловодске дешевле четырёхсот, покажи таблицей
  → FETCH [PLACES] WHERE @name IS 'Трактиръ На бульваре' && @price_rub BELOW 400 && @city IS 'Кисловодск' && @price_kind NOT 'per_night' AS TABLE
  # слот 202 · 4 условия · && · AS TABLE · предмет назван · поля @name @price_rub @city @price_kind · операторы IS BELOW NOT

- «На двоих» в Ессентуках дешевле четырёхсот, это не природный объект
  → FETCH [PLACES] WHERE @name IS 'На двоих' && @city IS 'Ессентуки' && @price_rub BELOW 400 && @category NOT 'nature'
  # слот 204 · 4 условия · && · без суффикса · предмет назван · поля @name @city @price_rub @category · операторы IS BELOW NOT

- «Корона», жильё дешевле девяти тысяч — таблицей
  → FETCH [PLACES] WHERE @name IS 'Корона' && @price_rub BELOW 9000 && @category IS 'lodging' && @price_kind NOT 'average_check' AS TABLE
  # слот 227 · 4 условия · && · AS TABLE · предмет назван · поля @name @price_rub @category @price_kind · операторы IS BELOW NOT

- «Мангал»: средний чек выше двухсот
  → FETCH [PLACES] WHERE @name IS 'Мангал' && @category IS 'food' && @price_kind IS 'average_check' && @price_rub ABOVE 200
  # слот 259 · 4 условия · && · без суффикса · предмет назван · поля @name @category @price_kind @price_rub · операторы IS ABOVE
