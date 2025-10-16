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

cd C:\Users\<ваше_имя>\PycharmProjects\perfume
3️⃣ Создать виртуальное окружение и активировать его

python -m venv .venv
.venv\Scripts\activate
4️⃣ Установить зависимости

pip install -r requirements.txt
5️⃣ Создать и инициализировать базу данных

python main.py init-db
📄 Добавление ссылок на товары
Откройте файл links.txt (создаётся в корне проекта).
Вставляйте ссылки построчно, вот примеры:

✅ Пример 1 — обычный список (каждая строка = один товар)
https://dnkparfum.ru/catalog/creed-aventus-parfyumernaya-voda-muzhskie-100ml/
https://dnkparfum.ru/catalog/attar-collection-crystal-love-parfyumernaya-voda-zhenskie-100ml/

✅ Пример 2 — один товар с фоллбэком (несколько зеркал через «|»)
https://site.com/product-a | https://mirror.site.com/product-a
💡 Комментарии начинающиеся с # и пустые строки игнорируются.

🚀 Запуск
1️⃣ Сбор данных (парсинг и запись в БД)

python main.py fetch --links links.txt
2️⃣ Формирование отчёта Excel

python main.py report
Отчёт сохраняется в файле price_report.xlsx в корне проекта.

Листы:

Текущие цены — последние значения и сравнение с предыдущими.

История — вся история изменений цен.

Легенда — пояснения, как читать таблицу.

🎨 Что означают цвета в отчёте
Цвет / столбец	Значение
🟩 Зелёный фон	Цена снизилась
🩷 Розовый фон	Цена выросла
Изменение (₽)	Разница с прошлой ценой
Изменение (%)	Относительное изменение в процентах
Когда проверено	Дата и время последнего обновления

⚠️ Частые ошибки и решения
Проблема	Причина / Решение
PermissionError: [Errno 13] Permission denied: 'price_report.xlsx'	Файл отчёта открыт в Excel. Закройте его и запустите команду ещё раз.
chromedriver not found	Установите Google Chrome и скачайте совместимый ChromeDriver, либо используйте Selenium Manager (встроен в новые версии).
ConnectionRefusedError или сайт не открывается	Проверьте доступность сайта и интернет-соединение.
Данные не сохраняются в БД	Убедитесь, что команда init-db выполнена успешно, и база price_tracker.sqlite3 существует.

⏰ Автоматический запуск (по желанию)
Можно добавить задачу в Планировщик задач Windows:

Программа: python

Аргументы: main.py fetch --links links.txt && python main.py report

Рабочая папка: путь к проекту

Расписание: ежедневно в нужное время.

🧩 Структура проекта
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
