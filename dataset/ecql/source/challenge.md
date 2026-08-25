# CHALLENGE

Ручной набор. Пятнадцать кейсов, рассчитанных на ручное заполнение и не
выводимых из шаблонов генерации. Целиком уходит в тест, в обучение не попадает.

Каждый кейс несёт признак, которого нет в обычных листах: число словами,
сокращение города, отрицание, вопрос вместо команды, значение на границе,
похожее слово с другим смыслом, фильтр по подстроке. Значения перечней
подобраны так, чтобы закрыть дефицит покрытия в тестовой выборке.

## Одно условие

- Что под охраной края, а не страны?
  → FETCH [PLACES] WHERE @heritage_status IS 'regional'
  # challenge · термин своими словами · вопрос вместо команды

- Достопримечательные места - именно места, не памятники
  → FETCH [PLACES] WHERE @object_kind IS 'heritage_site'
  # challenge · похожие слова с разным смыслом

- Отзывы, где обсуждают цену
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'цена'
  # challenge · похожее слово: цена как тема отзыва, а не @price_rub

- В каких отзывах вообще упоминают спа?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'спа'
  # challenge · фильтр по подстроке значения «бассейн и спа» · вопрос вместо команды

## Два условия

- Нужны вокзалы и станции Пятигорска, а не билеты
  → FETCH [PLACES] WHERE @city IS 'Пятигорск' && @category IS 'transport'
  # challenge · похожее слово: транспорт как объект, а не как способ проезда

- Купе куда угодно, кроме Москвы
  → FETCH [FARES] WHERE @fare_class IS 'kupe' && @route_end NOT 'Москва'
  # challenge · отрицание

- Чем занять ребёнка в Кисловодске?
  → FETCH [PLACES] WHERE @city IS 'Кисловодск' && @category IS 'activity'
  # challenge · вопрос вместо команды · предмет назван косвенно

- Где в Минводах закупиться сувенирами?
  → FETCH [PLACES] WHERE @city IS 'Минеральные Воды' && @category IS 'shopping'
  # challenge · сокращение города · вопрос вместо команды

- Источник ближе ста метров - бывает такое?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m BELOW 100
  # challenge · число словами · значение на границе · вопрос вместо команды

- У кого в отзывах про вайфай оценка ниже трёх?
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'wi-fi' && @rating BELOW 3
  # challenge · разговорное написание значения

- Четвёрки, в которых хвалят расположение
  → FETCH [REVIEWS] WHERE @aspects CONTAINS 'расположение' && @rating IS 4
  # challenge · оценка названа существительным

- Всё в Железноводске, кроме магазинов, просто назови списком
  → FETCH [PLACES] WHERE @city IS 'Железноводск' && @category NOT 'shopping' AS LIST
  # challenge · отрицание · суффикс вывода назван словами в конце фразы

## Три условия

- Долететь до Москвы экономом тысяч за десять - есть варианты?
  → FETCH [FARES] WHERE @route_end IS 'Москва' && @fare_class IS 'economy' && @price_rub BELOW 10000
  # challenge · число словами · вопрос вместо команды

- Развлечься бы не дальше пятисот метров от Колодца желаний
  → FETCH [PROXIMITY] WHERE @name IS 'Колодец желаний' && @neighbour_category IS 'activity' && @distance_m BELOW 500
  # challenge · число словами · имя в косвенном падеже

- Есть бытовые услуги не дальше трёхсот метров от Арабики?
  → FETCH [PROXIMITY] WHERE @name IS 'Арабика' && @neighbour_category IS 'service' && @distance_m BELOW 300
  # challenge · число словами · имя в косвенном падеже · вопрос вместо команды
