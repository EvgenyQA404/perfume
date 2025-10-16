# 💎 Price Tracker — мониторинг цен на парфюм (Selenium + SQLite + Excel)

Отслеживает цены на указанных сайтах и формирует Excel-отчёт.  
Работает на **Windows 10/11** с установленным **Python 3.11+**.

---

## ⚙️ Установка (первый запуск)

1️⃣ **Установить Python**

- Скачайте с [python.org/downloads](https://www.python.org/downloads/).

- При установке **обязательно поставьте галочку** ✅ “Add python.exe to PATH”.

2️⃣ **Склонировать или распаковать проект**

Скачайте проект из GitHub (или получите архив)  

и перейдите в его папку, например:

cd C:\Users\<ваше_имя>\perfume

3️⃣ **Создать виртуальное окружение и активировать его**

<pre>
python -m venv .venv
.venv\Scripts\activate
</pre>

4️⃣ **Установить зависимости**
<pre>
pip install -r requirements.txt
</pre>
5️⃣ **Создать и инициализировать базу данных**
<pre>
python main.py init-db
</pre>
📄 **Добавление ссылок на товары**

Откройте файл links.txt (создаётся в корне проекта).

Вставляйте ссылки построчно, вот примеры:

✅ Пример 1 — обычный список (каждая строка = один товар)
<pre>
https://dnkparfum.ru/catalog/creed-aventus-parfyumernaya-voda-muzhskie-100ml/

https://dnkparfum.ru/catalog/attar-collection-crystal-love-parfyumernaya-voda-zhenskie-100ml/
</pre>
✅ Пример 2 — один товар с фоллбэком (несколько зеркал через «|»)
<pre>
https://site.com/product-a | https://mirror.site.com/product-a
</pre>
💡 Комментарии начинающиеся с # и пустые строки игнорируются.

🚀 Запуск

1️⃣ **Сбор данных (парсинг и запись в БД)**
<pre>
python main.py fetch --links links.txt
</pre>

2️⃣ **Формирование отчёта Excel**
<pre>
python main.py report
</pre>
Отчёт сохраняется в файле price_report.xlsx в корне проекта.

Листы:

Текущие цены — последние значения и сравнение с предыдущими.

История — вся история изменений цен.

Легенда — пояснения, как читать таблицу.

🎨 **Что означают цвета в отчёте**

Цвет / столбец	Значение

🟩 Зелёный фон: Цена снизилась

🩷 Розовый фон: Цена выросла

Изменение (₽):	Разница с прошлой ценой

Изменение (%):	Относительное изменение в процентах

Когда проверено:	Дата и время последнего обновления

⚠️ **Частые ошибки и решения**

Проблема	Причина / Решение

PermissionError: [Errno 13] Permission denied: 'price_report.xlsx':	Файл отчёта открыт в Excel. Закройте его и запустите команду ещё раз.

chromedriver not found:	Установите Google Chrome и скачайте совместимый ChromeDriver, либо используйте Selenium Manager (встроен в новые версии).

ConnectionRefusedError или сайт не открывается:	Проверьте доступность сайта и интернет-соединение.

Данные не сохраняются в БД:	Убедитесь, что база price_tracker.sqlite3 существует.

🧩 **Структура проекта**
<pre>
perfume/
│
├── main.py              ← CLI-логика
├── db.py                ← SQLite-слой
├── report.py            ← генерация Excel
├── utils.py             ← парсер цен
├── locators.py          ← XPATH для Selenium
├── links.txt            ← список ссылок
├── price_tracker.sqlite3← база данных
└── price_report.xlsx    ← отчёт
</pre>
