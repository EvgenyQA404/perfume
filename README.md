# 💎 Price Tracker для сайта perfumex.ru (macOS, Chrome)

Эта программа автоматически заходит на сайт perfumex.ru, входит под вашим логином и паролем,
переходит по карточкам товаров и сохраняет цены в удобный Excel-отчёт с выделением изменений.

---

##🔧 Что понадобится

1️⃣ Компьютер с macOS (MacBook / iMac / Mac mini)

2️⃣ Google Chrome (браузер)

3️⃣ Интернет-соединение

4️⃣ Файл архива проекта (папка perfume)

5️⃣ Ваш логин и пароль от perfumex.ru

---

## 🪄 Установка пошагово

###🔹 1. Распакуйте архив

Сохраните предоставленный архив на рабочий стол и извлеките его.
Пусть итоговая папка называется perfume.

###🔹 2. Установите Python

Перейдите на сайт: https://www.python.org/downloads/mac-osx/

Скачайте версию Python 3.11.x (macOS 64-bit universal2 installer).

Установите (просто «Далее → Далее → Установить»).

После установки откройте Terminal (⌘ + пробел → напишите «Terminal» и нажмите Enter).

###🔹 3. Проверьте Python

В терминале вставьте команду:

<pre>python3 --version</pre>


Если появится что-то вроде:

<pre>Python 3.11.6</pre>


— значит, всё установлено успешно ✅

###🔹 4. Установите Google Chrome

Скачайте и установите браузер:
👉 https://www.google.com/chrome/

Chrome должен быть установлен в стандартную папку /Applications.

###🔹 5. Настройте секреты (логин и пароль)

В папке проекта perfume создайте файл secrets_perfumex.env.

Откройте его любым текстовым редактором (например, TextEdit).
Впишите туда свои данные от сайта perfumex.ru:

<pre>email=ваш_адрес@example.com
password=ВАШ_ПАРОЛЬ</pre>

Сохраните файл (⌘ + S).

###🔹 6. Добавьте ссылки на товары

Создайте (или откройте, если уже есть) файл links_perfumex.txt.
Каждая строка = один товар, например:

<pre>https://perfumex.ru/catalog/creed/creed_aventus_eau_de_parfum_100ml/</pre>

###🔹 7. Подготовьте среду

Откройте терминал и перейдите в папку проекта:

<pre>cd ~/Desktop/perfume</pre>

Теперь создайте виртуальное окружение и установите зависимости:

<pre>python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt</pre>

###🔹 8. Инициализируйте базу данных
<pre>python3 perfumex_main.py init-db</pre>


Появится файл perfumex.sqlite3 — в нём будут храниться цены и история.

---

### 🚀 Запуск парсера

Когда всё готово, выполните команду:

<pre>python3 perfumex_main.py fetch --links links_perfumex.txt --browser chrome</pre>

---

### 📊 Создание отчёта

После завершения сбора выполните команду:

<pre>python3 perfumex_main.py report</pre>


Будет создан файл perfumex_report.xlsx в той же папке.

⚠️ Если файл уже открыт в Excel или Numbers — закройте его и запустите команду снова.

---

### 🔁 Повторное использование

Можно запускать обновление хоть каждый день.
Просто выполняйте снова:

<pre>.venv/bin/python3 perfumex_main.py fetch --links links_perfumex.txt --browser chrome
.venv/bin/python3 perfumex_main.py report</pre>


История цен будет сохраняться — ничего не перезаписывается.

---
---

# 💎 Price Tracker для сайта dnkparfum.ru для macOS (Chrome и Яндекс.Браузер)

Это простая программа для отслеживания цен на парфюмерию и другие товары.  
Она автоматически открывает сайты, считывает цены и сохраняет отчёт в Excel.

---

## 🔧 Что понадобится

1️⃣ **Компьютер macOS (MacBook / iMac / Mac mini)**  
2️⃣ **Интернет**  
3️⃣ **Google Chrome или Яндекс.Браузер (любой один из них)**  
4️⃣ **Python 3.11 или новее**

---

## 🪄 Установка пошагово (для новичков)

### 🔹 1. Распакуйте архив
Сохраните предоставленный архив на рабочий стол,  
нажмите правой кнопкой → «Извлечь всё» или дважды щёлкните.

Пусть папка называется `perfume`.

---

### 🔹 2. Установите Python

1. Перейдите на сайт: [https://www.python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/)  
2. Скачайте версию **Python 3.11.x (macOS 64-bit universal2 installer)**  
3. Запустите установку (обычный двойной клик, далее → далее → установить).  
4. После установки откройте **Launchpad → Terminal** (терминал).  
   Можно найти через поиск Spotlight (⌘ + Пробел → введите «Terminal»).

### 🔹 3. Проверьте установку Python

Скопируйте и вставьте в терминал:
<pre>python3 --version</pre>
Если увидите вроде:
<pre>Python 3.11.6</pre>
значит всё ок

### 🔹 4. Установите Google Chrome (или Яндекс.Браузер)

Chrome: https://www.google.com/chrome/

(устанавливается как обычное приложение — перетащите в папку Applications).

Яндекс.Браузер: https://browser.yandex.ru/

После установки он появится как /Applications/Yandex.app.

### 🔹 5. Установите WebDriver

▪️ Вариант 1 — если используете Google Chrome

Ничего делать не нужно:
Selenium Manager автоматически скачает и настроит драйвер при первом запуске. 🎉

▪️ Вариант 2 — если используете Яндекс.Браузер

Скачайте драйвер yandexdriver с официального сайта:
👉 https://github.com/yandex/YandexDriver/releases

Распакуйте архив. Внутри будет файл yandexdriver.

Переместите его в папку /usr/local/bin (это системная папка для утилит).
Команда для этого в терминале:
<pre>sudo mv ~/Downloads/yandexdriver /usr/local/bin/
sudo chmod +x /usr/local/bin/yandexdriver</pre>
Проверьте, что драйвер установлен:
<pre>yandexdriver --version</pre>

### 🔹 6. Откройте проект в терминале

Если проект на рабочем столе:
<pre>cd ~/Desktop/perfume</pre>
Проверьте, что вы в нужной папке — команда:
<pre>ls</pre>
Должны увидеть файлы: main.py, requirements.txt, links.txt и т.д.

### 🔹 7. Установите зависимости (библиотеки)
<pre>python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt</pre>

### 🔹 8. Инициализируйте базу данных (разовое действие)
<pre>python3 main.py init-db</pre>
После этого появится файл price_tracker.sqlite3 — это база, где сохраняются цены.

---

### 🛒 Добавление ссылок

Откройте файл links.txt (двойной клик — откроется в «Текстовом редакторе»).

Каждая строка = один товар, пример:
<pre>https://dnkparfum.ru/catalog/creed-aventus-parfyumernaya-voda-muzhskie-100ml/
https://dnkparfum.ru/catalog/attar-collection-crystal-love-parfyumernaya-voda-zhenskie-100ml/</pre>

---

### 🚀 Запуск парсинга

Chrome
<pre>python3 main.py fetch --links links.txt --browser chrome
</pre>

Яндекс.Браузер
<pre>python3 main.py fetch --links links.txt --browser yandex --driver-path /usr/local/bin/yandexdriver
</pre>

(если установили yandexdriver в другую папку, замените путь)

---

### 📊 Формирование отчёта

После сбора данных сформируйте Excel-отчёт:
<pre>python3 main.py report
</pre>

Создастся файл price_report.xlsx в той же папке.

⚠️ Если он открыт в Numbers или Excel — закройте и повторите команду.

---

### ✅ Готово!

Теперь вы полностью готовы к работе:

Добавляете ссылки в links.txt

Выполняете python3 main.py fetch

Смотрите готовый отчёт price_report.xlsx

---

### 🚀 Как запускать в дальнейшем

Чтобы каждый раз не активировать виртуальное окружение, можно из корня проекта запускать напрямую.

1️⃣ Запуск парсера
<pre>.venv/bin/python main.py fetch --links links.txt --browser yandex --driver-path /usr/local/bin/yandexdriver
</pre>

2️⃣ Запуск отчёта
<pre>.venv/bin/python main.py report
</pre>

