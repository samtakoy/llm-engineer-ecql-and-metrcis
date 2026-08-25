# REVIEWS

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- В каких отзывах упоминают бассейн?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн'
  # добавлено вручную · одно условие · без связки · без суффикса · частичное совпадение · поля @aspects · операторы CONTAINS

- Что пишут про хостелы?
  → FETCH [REVIEWS] WHERE @object_class IS 'hostel'
  # слот 5 · одно условие · без связки · без суффикса · предмет назван · поля @object_class · операторы IS

- Где жалуются на шум?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'шум'
  # слот 23 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Ругают ли где-то чистоту?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'чистота'
  # слот 27 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Собери списком отзывы, где жалуются на шум.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'шум' AS LIST
  # слот 44 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Что говорят про расположение?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение'
  # слот 60 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Покажи отзывы о санаториях
  → FETCH [REVIEWS] WHERE @object_class IS 'sanatorium'
  # слот 62 · одно условие · без связки · без суффикса · предмет назван · поля @object_class · операторы IS

- Как отзываются о персонале? Перечисли списком.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' AS LIST
  # слот 69 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Где упоминают бассейн и спа?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа'
  # слот 87 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Что рассказывают про wi-fi в отзывах?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi'
  # слот 88 · одно условие · без связки · без суффикса · предмет назван · поля @aspects · операторы CONTAINS

- Отзывы с оценкой три
  → FETCH [REVIEWS] WHERE @rating IS 3
  # слот 90 · одно условие · без связки · без суффикса · поля @rating · операторы IS

- Списком бы отзывы, где говорят про wi-fi
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' AS LIST
  # слот 116 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Отзывы с оценкой один, нужен json
  → FETCH [REVIEWS] WHERE @rating IS 1 AS JSON
  # слот 131 · одно условие · без связки · AS JSON · поля @rating · операторы IS

- Хочу почитать отзывы, где поставили один балл.
  → FETCH [REVIEWS] WHERE @rating IS 1
  # слот 144 · одно условие · без связки · без суффикса · поля @rating · операторы IS

- Хочу списком почитать отзывы про завтраки
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' AS LIST
  # слот 158 · одно условие · без связки · AS LIST · предмет назван · поля @aspects · операторы CONTAINS

- Как отзываются о «Гостинном Дворе»?
  → FETCH [REVIEWS] WHERE @name IS 'Гостинный Двор'
  # слот 226 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

- Отзывы из Пятигорска сведи в таблицу
  → FETCH [REVIEWS] WHERE @city IS 'Пятигорск' AS TABLE
  # слот 239 · одно условие · без связки · AS TABLE · поля @city · операторы IS

- Какие отзывы оставляют о «Montis»?
  → FETCH [REVIEWS] WHERE @name IS 'Montis'
  # слот 260 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

## Два условия

- Хочу почитать отзывы по Пятигорску и Лермонтову.
  → FETCH [REVIEWS] WHERE @city IS 'Пятигорск' || @city IS 'Лермонтов'
  # слот 6 · 2 условия · || · без суффикса · поля @city · операторы IS

- Хочу понять, чем недовольны: найди отзывы с оценкой два, где упоминают завтрак.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' && @rating IS 2
  # слот 18 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Отзывы на четыре балла, где хвалят бассейн и спа
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа' && @rating IS 4
  # слот 22 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Выпиши списком отзывы с двойкой, в которых ругают персонал.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' && @rating IS 2 AS LIST
  # слот 28 · 2 условия · && · AS LIST · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Собери в таблицу отзывы на тройку, где говорят о чистоте.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'чистота' && @rating IS 3 AS TABLE
  # слот 34 · 2 условия · && · AS TABLE · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Покажи отзывы на хостелы, где упоминают бассейн и спа.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа' && @object_class IS 'hostel'
  # слот 65 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- Какие отзывы собрали санатории и отели?
  → FETCH [REVIEWS] WHERE @object_class IS 'sanatorium' || @object_class IS 'hotel'
  # слот 77 · 2 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

- Отбираю отель, интересны отзывы про бассейн и спа.
  → FETCH [REVIEWS] WHERE @object_class IS 'hotel' && @aspects CONTAINS 'бассейн и спа'
  # слот 85 · 2 условия · && · без суффикса · предмет назван · поля @object_class @aspects · операторы IS CONTAINS

- Кому из хостелов поставили три балла?
  → FETCH [REVIEWS] WHERE @object_class IS 'hostel' && @rating IS 3
  # слот 98 · 2 условия · && · без суффикса · предмет назван · поля @object_class @rating · операторы IS

- Хочу списком отзывы про хостелы и отели.
  → FETCH [REVIEWS] WHERE @object_class IS 'hostel' || @object_class IS 'hotel' AS LIST
  # слот 109 · 2 условия · || · AS LIST · предмет назван · поля @object_class · операторы IS

- Ищу санаторий, покажи отзывы, в которых упоминают парковку.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @object_class IS 'sanatorium'
  # слот 113 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- В санаториях есть wi-fi?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @object_class IS 'sanatorium'
  # слот 121 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- Хостелы: что там с расположением?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @object_class IS 'hostel'
  # слот 125 · 2 условия · && · без суффикса · предмет назван · поля @aspects @object_class · операторы CONTAINS IS

- Кому поставили один из-за расположения?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @rating IS 1
  # слот 129 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Отзывы, где номер оценили на пять
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @rating IS 5
  # слот 187 · 2 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS

- Пятёрочные отзывы о санаториях
  → FETCH [REVIEWS] WHERE @rating IS 5 && @object_class IS 'sanatorium'
  # слот 194 · 2 условия · && · без суффикса · предмет назван · поля @rating @object_class · операторы IS

- Отзывы о посуточной квартире в Железноводске
  → FETCH [REVIEWS] WHERE @name IS 'Квартира посуточно' && @city IS 'Железноводск'
  # слот 212 · 2 условия · && · без суффикса · предмет назван · поля @name @city · операторы IS

- Собери отзывы по Иноземцево, где цену не упоминают. Ответ списком.
  → FETCH [REVIEWS] WHERE @city IS 'Иноземцево' && @aspects NOT CONTAINS 'цена' AS LIST
  # слот 217 · 2 условия · && · AS LIST · предмет назван · поля @city @aspects · операторы IS NOT CONTAINS

- Нужны отзывы о гостевых домах или отелях.
  → FETCH [REVIEWS] WHERE @object_class IS 'guesthouse' || @object_class IS 'hotel'
  # слот 220 · 2 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

- Что в отзывах на «Оазис» говорят о чистоте?
  → FETCH [REVIEWS] WHERE @name IS 'Оазис' && @aspects CONTAINS 'чистота'
  # слот 228 · 2 условия · && · без суффикса · предмет назван · поля @name @aspects · операторы IS CONTAINS

- Отели и хостелы — просто назови списком
  → FETCH [REVIEWS] WHERE @object_class IS 'hotel' || @object_class IS 'hostel' AS LIST
  # слот 250 · 2 условия · || · AS LIST · предмет назван · поля @object_class · операторы IS

- Отели или гостевые дома
  → FETCH [REVIEWS] WHERE @object_class IS 'hotel' || @object_class IS 'guesthouse'
  # слот 252 · 2 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

## Три условия

- Нужны отзывы на отели, санатории и гостевые дома.
  → FETCH [REVIEWS] WHERE @object_class IS 'hotel' || @object_class IS 'sanatorium' || @object_class IS 'guesthouse'
  # слот 31 · 3 условия · || · без суффикса · предмет назван · поля @object_class · операторы IS

- Дай отзывы с оценкой три, где завтрак обсуждают, а шум не трогают.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'завтрак' && @rating IS 3 && @aspects NOT CONTAINS 'шум'
  # слот 33 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS NOT CONTAINS

- Ищу отели, где про персонал написали, а про номер - ни слова
  → FETCH [REVIEWS] WHERE @object_class IS 'hotel' && @aspects CONTAINS 'персонал' && @aspects NOT CONTAINS 'номер'
  # слот 91 · 3 условия · && · без суффикса · предмет назван · поля @object_class @aspects · операторы IS CONTAINS NOT CONTAINS

- Найди отзывы об отелях, где поставили два балла и о чистоте не написали.
  → FETCH [REVIEWS] WHERE @rating IS 2 && @object_class IS 'hotel' && @aspects NOT CONTAINS 'чистота'
  # слот 93 · 3 условия · && · без суффикса · предмет назван · поля @rating @object_class @aspects · операторы IS NOT CONTAINS

- Дай таблицу отзывов о гостевых домах, где wi-fi обсуждают, а цену не упоминают.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @object_class IS 'guesthouse' && @aspects NOT CONTAINS 'цена' AS TABLE
  # слот 105 · 3 условия · && · AS TABLE · предмет назван · поля @aspects @object_class · операторы CONTAINS IS NOT CONTAINS

- Найди отзывы на два балла, где парковку обсуждают, а шум не упоминают.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @rating IS 2 && @aspects NOT CONTAINS 'шум'
  # слот 123 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS NOT CONTAINS

- Какие отзывы из Кисловодска ставят четыре балла и говорят о цене?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена' && @rating IS 4 && @city IS 'Кисловодск'
  # слот 127 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating @city · операторы CONTAINS IS

- Что пишут про парковку в отзывах на четвёрку, если завтрак там не упоминают?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @rating IS 4 && @aspects NOT CONTAINS 'завтрак'
  # слот 136 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating · операторы CONTAINS IS NOT CONTAINS

- Собери таблицу отзывов на «Кэмэл Дом» с пятёркой за бассейн и спа.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'бассейн и спа' && @rating IS 5 && @name IS 'Кэмэл Дом' AS TABLE
  # слот 157 · 3 условия · && · AS TABLE · предмет назван · поля @aspects @rating @name · операторы CONTAINS IS

- Отзывы на отели Ессентуков покажи таблицей — те, где упоминают номер.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @object_class IS 'hotel' && @city IS 'Ессентуки' AS TABLE
  # слот 172 · 3 условия · && · AS TABLE · предмет назван · поля @aspects @object_class @city · операторы CONTAINS IS

- Кто поставил один в Минводах и жалуется на расположение?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @rating IS 1 && @city IS 'Минеральные Воды'
  # слот 185 · 3 условия · && · без суффикса · предмет назван · поля @aspects @rating @city · операторы CONTAINS IS

- Мне нужны отзывы вне городов с оценкой выше четырёх баллов, и чтобы цену в них не упоминали.
  → FETCH [REVIEWS] WHERE @city IS 'вне городов' && @aspects NOT CONTAINS 'цена' && @rating ABOVE 4
  # слот 237 · 3 условия · && · без суффикса · предмет назван · поля @city @aspects @rating · операторы IS NOT CONTAINS ABOVE

- Что говорят про «Пассаж» в Ессентуках? Про чистоту ничего не надо — сведи в таблицу
  → FETCH [REVIEWS] WHERE @name IS 'Пассаж' && @city IS 'Ессентуки' && @aspects NOT CONTAINS 'чистота' AS TABLE
  # слот 238 · 3 условия · && · AS TABLE · предмет назван · поля @name @city @aspects · операторы IS NOT CONTAINS

- Покажи списком, что говорят про «Орлиные скалы» в Лермонтове там, где про завтрак не пишут
  → FETCH [REVIEWS] WHERE @name IS 'Орлиные скалы' && @city IS 'Лермонтов' && @aspects NOT CONTAINS 'завтрак' AS LIST
  # слот 244 · 3 условия · && · AS LIST · предмет назван · поля @name @city @aspects · операторы IS NOT CONTAINS

- Читаю про «Теплый стан» в Минеральных Водах — нужны отзывы, где расположение не упоминают.
  → FETCH [REVIEWS] WHERE @name IS 'Теплый стан' && @city IS 'Минеральные Воды' && @aspects NOT CONTAINS 'расположение'
  # слот 253 · 3 условия · && · без суффикса · предмет назван · поля @name @city @aspects · операторы IS NOT CONTAINS

## Четыре условия

- Где за номер поставили два, про завтрак в отзыве молчат, и это не санаторий?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @rating IS 2 && @aspects NOT CONTAINS 'завтрак' && @object_class NOT 'sanatorium'
  # слот 10 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @object_class · операторы CONTAINS IS NOT CONTAINS NOT

- Беру гостевой дом на пятёрку, где про шум пишут, а про парковку молчат — списком.
  → FETCH [REVIEWS] WHERE @object_class IS 'guesthouse' && @rating IS 5 && @aspects NOT CONTAINS 'парковка' && @aspects CONTAINS 'шум' AS LIST
  # слот 16 · 4 условия · && · AS LIST · предмет назван · поля @object_class @rating @aspects · операторы IS NOT CONTAINS CONTAINS

- Собираю отзывы на три балла с упоминанием wi-fi, где про бассейн и спа не пишут и речь не о гостевом доме.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @rating IS 3 && @aspects NOT CONTAINS 'бассейн и спа' && @object_class NOT 'guesthouse'
  # слот 38 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @object_class · операторы CONTAINS IS NOT CONTAINS NOT

- Отзывы об отелях: пишут о персонале, цену не трогают, оценка не один
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' && @object_class IS 'hotel' && @aspects NOT CONTAINS 'цена' && @rating NOT 1
  # слот 48 · 4 условия · && · без суффикса · предмет назван · поля @aspects @object_class @rating · операторы CONTAINS IS NOT CONTAINS NOT

- Что пишут о гостевых домах про цену, если оценка не четыре и расположение не обсуждают?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена' && @object_class IS 'guesthouse' && @rating NOT 4 && @aspects NOT CONTAINS 'расположение'
  # слот 100 · 4 условия · && · без суффикса · предмет назван · поля @aspects @object_class @rating · операторы CONTAINS IS NOT NOT CONTAINS

- Собираюсь в Кисловодск — покажи отзывы про цену в гостевых домах, кроме тех, где поставили один.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена' && @object_class IS 'guesthouse' && @rating NOT 1 && @city IS 'Кисловодск'
  # слот 107 · 4 условия · && · без суффикса · предмет назван · поля @aspects @object_class @rating @city · операторы CONTAINS IS NOT

- В Кисловодске ищу отзывы на пятёрку, где пишут про парковку и ни слова про wi-fi.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'парковка' && @rating IS 5 && @aspects NOT CONTAINS 'wi-fi' && @city IS 'Кисловодск'
  # слот 160 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @city · операторы CONTAINS IS NOT CONTAINS

- Дай списком отзывы о санатории «Санаторий-профилакторий РЖД»: про номера пишут, про расположение не пишут
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'номер' && @object_class IS 'sanatorium' && @name IS 'Санаторий-профилакторий РЖД' && @aspects NOT CONTAINS 'расположение' AS LIST
  # слот 175 · 4 условия · && · AS LIST · предмет назван · поля @aspects @object_class @name · операторы CONTAINS IS NOT CONTAINS

- Расскажи про персонал «Евразии» в Пятигорске по отзывам на четыре балла.
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'персонал' && @rating IS 4 && @name IS 'Евразия' && @city IS 'Пятигорск'
  # слот 186 · 4 условия · && · без суффикса · предмет назван · поля @aspects @rating @name @city · операторы CONTAINS IS

- Ищу отзывы об «Отель Pechorinn» в Железноводске, где не единица и молчат про бассейн и спа.
  → FETCH [REVIEWS] WHERE @name IS 'Отель Pechorinn' && @city IS 'Железноводск' && @aspects NOT CONTAINS 'бассейн и спа' && @rating NOT 1
  # слот 232 · 4 условия · && · без суффикса · предмет назван · поля @name @city @aspects @rating · операторы IS NOT CONTAINS NOT

- Что говорят о «Курортных историях» в Ессентуках, если это не хостел и расположение не упоминают?
  → FETCH [REVIEWS] WHERE @name IS 'Курортные истории' && @city IS 'Ессентуки' && @aspects NOT CONTAINS 'расположение' && @object_class NOT 'hostel'
  # слот 246 · 4 условия · && · без суффикса · предмет назван · поля @name @city @aspects @object_class · операторы IS NOT CONTAINS NOT
