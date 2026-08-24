# PROXIMITY

Вопрос пишется человеком, строка ECQL и строка разметки после неё -
результат генерации. Перезапуск генератора вопросы сохраняет.

## Одно условие

- Что из еды поблизости?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food'
  # слот 29 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Транспорт рядом
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport'
  # слот 40 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Чем заняться рядом?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity'
  # слот 126 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Жильё поблизости
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging'
  # слот 135 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Источники по соседству, json
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' AS JSON
  # слот 139 · одно условие · без связки · AS JSON · предмет назван · поля @neighbour_category · операторы IS

- Какие услуги рядом?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service'
  # слот 140 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Развлечения рядом — дай в json
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' AS JSON
  # слот 164 · одно условие · без связки · AS JSON · предмет назван · поля @neighbour_category · операторы IS

- Что культурного рядом?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture'
  # слот 176 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Источники поблизости
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water'
  # слот 178 · одно условие · без связки · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Что дальше шестидесяти метров?
  → FETCH [PROXIMITY] WHERE @distance_m ABOVE 60
  # слот 243 · одно условие · без связки · без суффикса · поля @distance_m · операторы ABOVE

- Что рядом с домом Разумовского?
  → FETCH [PROXIMITY] WHERE @name IS 'Дом Разумовского В. И.'
  # слот 255 · одно условие · без связки · без суффикса · предмет назван · поля @name · операторы IS

## Два условия

- Развлечения в паре минут ходьбы
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' && @distance_m BELOW 170
  # слот 19 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Рядом еда или природа
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food' || @neighbour_category IS 'nature'
  # слот 20 · 2 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Услуги в десяти минутах ходьбы, списком
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service' && @distance_m BELOW 800 AS LIST
  # слот 25 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Где переночевать рядом с домом, где жил Умар Алиев?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging' && @name IS 'В этом доме жил Умар Джашуевич Алиев'
  # слот 72 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @name · операторы IS

- Где поесть рядом с «Арабикой»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food' && @name IS 'Арабика'
  # слот 118 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @name · операторы IS

- Транспорт в пяти минутах — нужен список
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport' && @distance_m BELOW 300 AS LIST
  # слот 133 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Услуги дальше двухсот метров
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service' && @distance_m ABOVE 200
  # слот 138 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Природа в пятнадцати минутах ходьбы, просто назови списком
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'nature' && @distance_m BELOW 1100 AS LIST
  # слот 143 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Культура дальше шестисот метров — в таблицу
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' && @distance_m ABOVE 600 AS TABLE
  # слот 153 · 2 условия · && · AS TABLE · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Услуги в пяти минутах
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'service' && @distance_m BELOW 300
  # слот 156 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Рядом магазины или культура
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' || @neighbour_category IS 'culture'
  # слот 159 · 2 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Еда прямо вплотную, метрах в двадцати
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'food' && @distance_m BELOW 20
  # слот 166 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Жильё дальше сотни метров
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging' && @distance_m ABOVE 100
  # слот 168 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Культурные объекты в десяти минутах ходьбы, сведи таблицей
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' && @distance_m BELOW 700 AS TABLE
  # слот 174 · 2 условия · && · AS TABLE · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Источники в пятистах метрах
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m BELOW 500
  # слот 188 · 2 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m · операторы IS BELOW

- Источники дальше четырёхсот метров, списком
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m ABOVE 400 AS LIST
  # слот 191 · 2 условия · && · AS LIST · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE

- Что дальше шестисот метров от «Ventuno»?
  → FETCH [PROXIMITY] WHERE @name IS 'Ventuno' && @distance_m ABOVE 600
  # слот 210 · 2 условия · && · без суффикса · предмет назван · поля @name @distance_m · операторы IS ABOVE

- Что в четырёхстах метрах от храма Смоленской иконы? Списком
  → FETCH [PROXIMITY] WHERE @name IS 'Храм Смоленской иконы Божией Матери' && @distance_m BELOW 400 AS LIST
  # слот 221 · 2 условия · && · AS LIST · предмет назван · поля @name @distance_m · операторы IS BELOW

- Природа в десяти минутах ходьбы
  → FETCH [PROXIMITY] WHERE @distance_m BELOW 800 && @neighbour_category IS 'nature'
  # слот 222 · 2 условия · && · без суффикса · предмет назван · поля @distance_m @neighbour_category · операторы BELOW IS

- Что дальше семидесяти метров от особняка Милашевских?
  → FETCH [PROXIMITY] WHERE @name IS 'Особняк Милашевских' && @distance_m ABOVE 70
  # слот 223 · 2 условия · && · без суффикса · предмет назван · поля @name @distance_m · операторы IS ABOVE

- Что дальше двухсот метров, кроме культурных объектов?
  → FETCH [PROXIMITY] WHERE @distance_m ABOVE 200 && @neighbour_category NOT 'culture'
  # слот 225 · 2 условия · && · без суффикса · предмет назван · поля @distance_m @neighbour_category · операторы ABOVE NOT

- Что в пятнадцати минутах от «Palazzo»?
  → FETCH [PROXIMITY] WHERE @name IS 'Palazzo' && @distance_m BELOW 1200
  # слот 235 · 2 условия · && · без суффикса · предмет назван · поля @name @distance_m · операторы IS BELOW

- Культура дальше километра с лишним
  → FETCH [PROXIMITY] WHERE @distance_m ABOVE 1300 && @neighbour_category IS 'culture'
  # слот 242 · 2 условия · && · без суффикса · предмет назван · поля @distance_m @neighbour_category · операторы ABOVE IS

## Три условия

- Культура, природа и услуги рядом — одним списком
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' || @neighbour_category IS 'nature' || @neighbour_category IS 'service' AS LIST
  # слот 39 · 3 условия · || · AS LIST · предмет назван · поля @neighbour_category · операторы IS

- Рядом магазины, транспорт или жильё
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' || @neighbour_category IS 'transport' || @neighbour_category IS 'lodging'
  # слот 42 · 3 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Природа от километра до полутора, покажи таблицей
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'nature' && @distance_m ABOVE 1000 && @distance_m BELOW 1500 AS TABLE
  # слот 45 · 3 условия · && · AS TABLE · диапазон · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE BELOW

- Развлечения метрах в ста семидесяти
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' && @distance_m ABOVE 160 && @distance_m BELOW 180
  # слот 49 · 3 условия · && · без суффикса · диапазон · предмет назван · поля @neighbour_category @distance_m · операторы IS ABOVE BELOW

- Транспорт в паре шагов от памятника Ленину, списочком
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport' && @name IS 'В.И. Ленину' && @distance_m BELOW 140 AS LIST
  # слот 83 · 3 условия · && · AS LIST · предмет назван · поля @neighbour_category @name @distance_m · операторы IS BELOW

- Магазины дальше ста тридцати метров от «Ресторана Парк»
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' && @name IS 'Ресторан Парк' && @distance_m ABOVE 130
  # слот 112 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @name @distance_m · операторы IS ABOVE

- Транспорт дальше ста двадцати метров от памятника Ленину
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'transport' && @name IS 'В.И. Ленину' && @distance_m ABOVE 120
  # слот 115 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @name @distance_m · операторы IS ABOVE

- Культура в десяти минутах от «Мини отеля» — сравни в таблице
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' && @name IS 'Мини отель' && @distance_m BELOW 700 AS TABLE
  # слот 124 · 3 условия · && · AS TABLE · предмет назван · поля @neighbour_category @name @distance_m · операторы IS BELOW

- Жильё в ста метрах от дома Умара Алиева, нужен json
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'lodging' && @distance_m BELOW 110 && @name IS 'В этом доме жил Умар Джашуевич Алиев' AS JSON
  # слот 130 · 3 условия · && · AS JSON · предмет назван · поля @neighbour_category @distance_m @name · операторы IS BELOW

- Развлечения дальше ста шестидесяти метров от студии «Время творить»
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'activity' && @name IS 'Творческая студия «Время творить»' && @distance_m ABOVE 160
  # слот 165 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @name @distance_m · операторы IS ABOVE

- Что из магазинов дальше ста тридцати метров от «Ресторана Парк»?
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' && @distance_m ABOVE 130 && @name IS 'Ресторан Парк'
  # слот 167 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m @name · операторы IS ABOVE

- Магазины в ста сорока метрах от «Ресторана Парк»
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' && @distance_m BELOW 140 && @name IS 'Ресторан Парк'
  # слот 170 · 3 условия · && · без суффикса · предмет назван · поля @neighbour_category @distance_m @name · операторы IS BELOW

- Что дальше двухсот метров от «DunCan Lounge», кроме жилья?
  → FETCH [PROXIMITY] WHERE @name IS 'DunCan Lounge' && @distance_m ABOVE 200 && @neighbour_category NOT 'lodging'
  # слот 200 · 3 условия · && · без суффикса · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

- Далеко от антикафе «Песочница», больше километра, жильё не нужно
  → FETCH [PROXIMITY] WHERE @name IS 'Антикафе "Песочница"' && @distance_m ABOVE 1100 && @neighbour_category NOT 'lodging'
  # слот 201 · 3 условия · && · без суффикса · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

- Культура, природа или жильё рядом
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'culture' || @neighbour_category IS 'nature' || @neighbour_category IS 'lodging'
  # слот 203 · 3 условия · || · без суффикса · предмет назван · поля @neighbour_category · операторы IS

- Дальше ста восьмидесяти метров от «Суши хаус», без развлечений — json
  → FETCH [PROXIMITY] WHERE @name IS 'Суши хаус' && @distance_m ABOVE 180 && @neighbour_category NOT 'activity' AS JSON
  # слот 224 · 3 условия · && · AS JSON · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

- Магазины, еда и природа рядом — списком
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'shopping' || @neighbour_category IS 'food' || @neighbour_category IS 'nature' AS LIST
  # слот 236 · 3 условия · || · AS LIST · предмет назван · поля @neighbour_category · операторы IS

- Соседи лютеранской кирхи в двухстах метрах, развлечения не считаем — таблицей
  → FETCH [PROXIMITY] WHERE @name IS 'Ансамбль лютеранской кирхи' && @distance_m BELOW 190 && @neighbour_category NOT 'activity' AS TABLE
  # слот 251 · 3 условия · && · AS TABLE · предмет назван · поля @name @distance_m @neighbour_category · операторы IS BELOW NOT

- Что дальше ста десяти метров от колодца желаний, жильё не нужно
  → FETCH [PROXIMITY] WHERE @name IS 'Колодец желаний' && @distance_m ABOVE 110 && @neighbour_category NOT 'lodging'
  # слот 258 · 3 условия · && · без суффикса · предмет назван · поля @name @distance_m @neighbour_category · операторы IS ABOVE NOT

## Четыре условия

- Природа рядом со «Вторым дедом», примерно в километре, нужен список
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'nature' && @distance_m ABOVE 1000 && @distance_m BELOW 1200 && @name IS 'Второй дед' AS LIST
  # слот 12 · 4 условия · && · AS LIST · диапазон · предмет назван · поля @neighbour_category @distance_m @name · операторы IS ABOVE BELOW

- Источники метрах в ста от памятника Пушкину
  → FETCH [PROXIMITY] WHERE @neighbour_category IS 'water' && @distance_m ABOVE 90 && @distance_m BELOW 120 && @name IS 'А. С. Пушкин'
  # слот 52 · 4 условия · && · без суффикса · диапазон · предмет назван · поля @neighbour_category @distance_m @name · операторы IS ABOVE BELOW
