# REVIEWS

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Где есть бассейн?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн'
  # добавлено вручную · одно условие · без связки · без суффикса · частичное совпадение · поля @aspects · операторы CONTAINS

- Что пишут про хостелы?
  → FETCH [REVIEWS] WHERE @object_class IS 'хостел'
  # слот 5 · одно условие · без связки · без суффикса · предмет назван · поля @object_class · операторы IS

- Где жалуются на шум?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'шум'
  # слот 23 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Что пишут про чистоту?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'чистота'
  # слот 27 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Отзывы про шум, списком
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'шум' AS LIST
  # слот 44 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Что говорят про расположение?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение'
  # слот 60 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Отзывы о санаториях
  → FETCH [REVIEWS] WHERE @object_class IS 'санаторий'
  # слот 62 · одно условие · без связки · без суффикса · предмет назван · поля @object_class · операторы IS

- Что пишут о персонале? Списком
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' AS LIST
  # слот 69 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Где упоминают бассейн и спа?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа'
  # слот 87 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Что пишут про wi-fi?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi'
  # слот 88 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Отзывы с оценкой три
  → FETCH [REVIEWS] WHERE @rating IS 3
  # слот 90 · одно условие · без связки · без суффикса · поля @rating · операторы IS

- Отзывы про wi-fi — одним списком
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' AS LIST
  # слот 116 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Отзывы с оценкой один, нужен json
  → FETCH [REVIEWS] WHERE @rating IS 1 AS JSON
  # слот 131 · одно условие · без связки · AS JSON · поля @rating · операторы IS

- Отзывы с самой низкой оценкой
  → FETCH [REVIEWS] WHERE @rating IS 1
  # слот 144 · одно условие · без связки · без суффикса · поля @rating · операторы IS

- Про завтрак что пишут, списком
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' AS LIST
  # слот 158 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Что пишут про «Гостинный Двор»?
  → FETCH [REVIEWS] WHERE @name IS 'Гостинный Двор'
  # слот 226 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

- Отзывы из Пятигорска сведи в таблицу
  → FETCH [REVIEWS] WHERE @city IS 'Пятигорск' AS TABLE
  # слот 239 · одно условие · без связки · AS TABLE · поля @city · операторы IS

- Что известно про «Montis»?
  → FETCH [REVIEWS] WHERE @name IS 'Montis'
  # слот 260 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

## Два условия

- Отзывы из Пятигорска и Лермонтова
  → FETCH [REVIEWS] WHERE @city IS 'Пятигорск' || @city IS 'Лермонтов'
  # слот 6 · 2 условия · || · без суффикса · поля @city · операторы IS

- Кто поставил два и ругает завтрак?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' && @rating IS 2
  # слот 18 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Отзывы на четыре балла, где хвалят бассейн и спа
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа' && @rating IS 4
  # слот 22 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Оценка два и претензия к персоналу — списком
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' && @rating IS 2 AS LIST
  # слот 28 · 2 условия · && · AS LIST · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Оценка три, речь о чистоте — в таблицу
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'чистота' && @rating IS 3 AS TABLE
  # слот 34 · 2 условия · && · AS TABLE · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- В хостелах пишут про бассейн и спа?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа' && @object_class IS 'хостел'
  # слот 65 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- Санатории или отели
  → FETCH [REVIEWS] WHERE @object_class IS 'санаторий' || @object_class IS 'отель'
  # слот 77 · 2 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

- Отели, где есть бассейн и спа
  → FETCH [REVIEWS] WHERE @object_class IS 'отель' && @aspects CONTAINS 'бассейн и спа'
  # слот 85 · 2 условия · && · без суффикса · предмет назван · поля @object_class @aspects · операторы IS CONTAINS

- Отзывы о хостелах на три
  → FETCH [REVIEWS] WHERE @object_class IS 'хостел' && @rating IS 3
  # слот 98 · 2 условия · && · без суффикса · предмет назван · поля @object_class @rating · операторы IS

- Хостелы и отели, списочком
  → FETCH [REVIEWS] WHERE @object_class IS 'хостел' || @object_class IS 'отель' AS LIST
  # слот 109 · 2 условия · || · AS LIST · предмет назван · поля @object_class · операторы IS

- Санатории с парковкой
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @object_class IS 'санаторий'
  # слот 113 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- В санаториях есть wi-fi?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @object_class IS 'санаторий'
  # слот 121 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- Хостелы: что там с расположением?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @object_class IS 'хостел'
  # слот 125 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- Кому поставили один из-за расположения?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @rating IS 1
  # слот 129 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Отзывы, где номер оценили на пять
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @rating IS 5
  # слот 187 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Пятёрочные отзывы о санаториях
  → FETCH [REVIEWS] WHERE @rating IS 5 && @object_class IS 'санаторий'
  # слот 194 · 2 условия · && · без суффикса · предмет назван · поля @rating @object_class · операторы IS

- Отзывы о посуточной квартире в Железноводске
  → FETCH [REVIEWS] WHERE @name IS 'Квартира посуточно' && @city IS 'Железноводск'
  # слот 212 · 2 условия · && · без суффикса · предмет назван · поля @name @city · операторы IS

- Иноземцево, цену не обсуждают — нужен список
  → FETCH [REVIEWS] WHERE @city IS 'Иноземцево' && @aspects NOT CONTAINS 'цена' AS LIST
  # слот 217 · 2 условия · && · AS LIST · предмет назван · поля @city @aspects · операторы IS NOT CONTAINS

- Гостевые дома или отели
  → FETCH [REVIEWS] WHERE @object_class IS 'гостевой дом' || @object_class IS 'отель'
  # слот 220 · 2 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

- «Оазис» — что там с чистотой?
  → FETCH [REVIEWS] WHERE @name IS 'Оазис' && @aspects CONTAINS 'чистота'
  # слот 228 · 2 условия · && · без суффикса · предмет назван · поля @name @aspects · операторы IS CONTAINS

- Отели и хостелы — просто назови списком
  → FETCH [REVIEWS] WHERE @object_class IS 'отель' || @object_class IS 'хостел' AS LIST
  # слот 250 · 2 условия · || · AS LIST · предмет назван · поля @object_class · операторы IS

- Отели или гостевые дома
  → FETCH [REVIEWS] WHERE @object_class IS 'отель' || @object_class IS 'гостевой дом'
  # слот 252 · 2 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

## Три условия

- Отели, санатории или гостевые дома
  → FETCH [REVIEWS] WHERE @object_class IS 'отель' || @object_class IS 'санаторий' || @object_class IS 'гостевой дом'
  # слот 31 · 3 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

- Оценка три, речь о завтраке, шум не упоминается
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' && @rating IS 3 && @aspects NOT CONTAINS 'шум'
  # слот 33 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS NOT CONTAINS

- Отели: про персонал пишут, про номер нет
  → FETCH [REVIEWS] WHERE @object_class IS 'отель' && @aspects CONTAINS 'персонал' && @aspects NOT CONTAINS 'номер'
  # слот 91 · 3 условия · && · без суффикса · предмет назван · поля @object_class @aspects · операторы IS CONTAINS NOT CONTAINS

- Отзывы об отелях на два, чистота не упомянута
  → FETCH [REVIEWS] WHERE @rating IS 2 && @object_class IS 'отель' && @aspects NOT CONTAINS 'чистота'
  # слот 93 · 3 условия · && · без суффикса · предмет назван · поля @rating @object_class @aspects · операторы IS NOT CONTAINS

- Гостевые дома с wi-fi, цену не упоминают — таблицей
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @object_class IS 'гостевой дом' && @aspects NOT CONTAINS 'цена' AS TABLE
  # слот 105 · 3 условия · && · AS TABLE · предмет назван · поля @aspects @object_class · операторы CONTAINS IS NOT CONTAINS

- Оценка два, речь о парковке, а шума нет
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @rating IS 2 && @aspects NOT CONTAINS 'шум'
  # слот 123 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS NOT CONTAINS

- Четыре балла в Кисловодске, где обсуждают цену
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена' && @rating IS 4 && @city IS 'Кисловодск'
  # слот 127 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating @city · операторы CONTAINS IS

- Отзывы на четыре про парковку, завтрак не упомянут
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @rating IS 4 && @aspects NOT CONTAINS 'завтрак'
  # слот 136 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS NOT CONTAINS

- «Кэмэл Дом», пятёрки за бассейн и спа — сравни в таблице
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа' && @rating IS 5 && @name IS 'Кэмэл Дом' AS TABLE
  # слот 157 · 3 условия · && · AS TABLE · предмет назван · поля @aspects @rating @name · операторы CONTAINS IS

- Отели Ессентуков, где пишут про номер — табличкой
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @object_class IS 'отель' && @city IS 'Ессентуки' AS TABLE
  # слот 172 · 3 условия · && · AS TABLE · предмет назван · поля @aspects @object_class @city · операторы CONTAINS IS

- Кто поставил один в Минводах из-за расположения?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @rating IS 1 && @city IS 'Минеральные Воды'
  # слот 185 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating @city · операторы CONTAINS IS

- Загородные, оценка выше четырёх, цену не упоминают
  → FETCH [REVIEWS] WHERE @city IS 'вне городов' && @aspects NOT CONTAINS 'цена' && @rating ABOVE 4
  # слот 237 · 3 условия · && · без суффикса · предмет назван · поля @city @aspects @rating · операторы IS NOT CONTAINS ABOVE

- «Пассаж» в Ессентуках, чистота не упомянута — в таблицу
  → FETCH [REVIEWS] WHERE @name IS 'Пассаж' && @city IS 'Ессентуки' && @aspects NOT CONTAINS 'чистота' AS TABLE
  # слот 238 · 3 условия · && · AS TABLE · предмет назван · поля @name @city @aspects · операторы IS NOT CONTAINS

- «Орлиные скалы» в Лермонтове, завтрак не обсуждают, списком
  → FETCH [REVIEWS] WHERE @name IS 'Орлиные скалы' && @city IS 'Лермонтов' && @aspects NOT CONTAINS 'завтрак' AS LIST
  # слот 244 · 3 условия · && · AS LIST · предмет назван · поля @name @city @aspects · операторы IS NOT CONTAINS

- «Теплый стан» в Минеральных Водах, расположение не обсуждают
  → FETCH [REVIEWS] WHERE @name IS 'Теплый стан' && @city IS 'Минеральные Воды' && @aspects NOT CONTAINS 'расположение'
  # слот 253 · 3 условия · && · без суффикса · предмет назван · поля @name @city @aspects · операторы IS NOT CONTAINS

## Четыре условия

- Оценка два за номер, про завтрак ни слова, санатории не нужны
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @rating IS 2 && @aspects NOT CONTAINS 'завтрак' && @object_class NOT 'санаторий'
  # слот 10 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @object_class · операторы CONTAINS IS NOT CONTAINS NOT

- Гостевые дома на пять, шум упомянут, парковки нет — списком
  → FETCH [REVIEWS] WHERE @object_class IS 'гостевой дом' && @rating IS 5 && @aspects NOT CONTAINS 'парковка' && @aspects CONTAINS 'шум' AS LIST
  # слот 16 · 4 условия · && · AS LIST · предмет назван · поля @object_class @rating @aspects · операторы IS NOT CONTAINS CONTAINS

- Оценка три про wi-fi, без спа и не в гостевых домах
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @rating IS 3 && @aspects NOT CONTAINS 'бассейн и спа' && @object_class NOT 'гостевой дом'
  # слот 38 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @object_class · операторы CONTAINS IS NOT CONTAINS NOT

- Отзывы об отелях: пишут о персонале, цену не трогают, оценка не один
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' && @object_class IS 'отель' && @aspects NOT CONTAINS 'цена' && @rating NOT 1
  # слот 48 · 4 условия · && · без суффикса · предмет назван · поля @aspects @object_class @rating · операторы CONTAINS IS NOT CONTAINS NOT

- Отзывы о гостевых домах: речь о цене, оценка не четыре, расположение не обсуждают
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена' && @object_class IS 'гостевой дом' && @rating NOT 4 && @aspects NOT CONTAINS 'расположение'
  # слот 100 · 4 условия · && · без суффикса · предмет назван · поля @aspects @object_class @rating · операторы CONTAINS IS NOT NOT CONTAINS

- Отзывы о гостевых домах Кисловодска: о цене, но оценка не один
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена' && @object_class IS 'гостевой дом' && @rating NOT 1 && @city IS 'Кисловодск'
  # слот 107 · 4 условия · && · без суффикса · предмет назван · поля @aspects @object_class @rating @city · операторы CONTAINS IS NOT

- Кисловодск, оценка пять за парковку, wi-fi не упоминают
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @rating IS 5 && @aspects NOT CONTAINS 'wi-fi' && @city IS 'Кисловодск'
  # слот 160 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @city · операторы CONTAINS IS NOT CONTAINS

- Номера в санатории-профилактории РЖД — нужен список отзывов
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @object_class IS 'санаторий' && @name IS 'Санаторий-профилакторий РЖД' && @aspects NOT CONTAINS 'расположение' AS LIST
  # слот 175 · 4 условия · && · AS LIST · предмет назван · поля @aspects @object_class @name · операторы CONTAINS IS NOT CONTAINS

- Что пишут про персонал «Евразии» в Пятигорске в отзывах на четыре?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' && @rating IS 4 && @name IS 'Евразия' && @city IS 'Пятигорск'
  # слот 186 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @name @city · операторы CONTAINS IS

- Отзывы об «Отель Pechorinn» в Железноводске: без спа, оценка не один
  → FETCH [REVIEWS] WHERE @name IS 'Отель Pechorinn' && @city IS 'Железноводск' && @aspects NOT CONTAINS 'бассейн и спа' && @rating NOT 1
  # слот 232 · 4 условия · && · без суффикса · предмет назван · поля @name @city @aspects @rating · операторы IS NOT CONTAINS NOT

- «Курортные истории» в Ессентуках: не хостел, расположение не упомянуто
  → FETCH [REVIEWS] WHERE @name IS 'Курортные истории' && @city IS 'Ессентуки' && @aspects NOT CONTAINS 'расположение' && @object_class NOT 'хостел'
  # слот 246 · 4 условия · && · без суффикса · предмет назван · поля @name @city @aspects @object_class · операторы IS NOT CONTAINS NOT
