# perfumex_main.py — отдельный парсер для perfumex.ru

import argparse
import os
import re
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import perfumex_db as db
import perfumex_locators as L
from perfumex_utils import parse_price_and_currency, load_env_kv

DEFAULT_LINKS_FILE = Path("links_perfumex.txt")
DEFAULT_SECRETS_FILE = Path("secrets_perfumex.env")
BASE_URL = "https://perfumex.ru/"


def load_links_txt(links_file: Path) -> List[List[str]]:
    """
    1 строка = 1 товар; фоллбэки через '|'
    Возвращает список групп URL: List[List[str]]
    """
    if not links_file.exists():
        return []
    groups = []
    for raw in links_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in re.split(r"\s*\|\s*", line) if p.strip()]
        if parts:
            groups.append(parts)
    return groups


def build_driver(browser: str = "chrome",
                 headless: bool = True,
                 driver_path: str | None = None) -> webdriver.Chrome:
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless=new")

    if browser.lower() == "yandex":
        # Попытка найти бинарь Яндекс.Браузера (macOS)
        for p in ["/Applications/Yandex.app/Contents/MacOS/Yandex",
                  "/Applications/Yandex Browser.app/Contents/MacOS/Yandex"]:
            if Path(p).exists():
                options.binary_location = p
                break
        # Явный путь к yandexdriver при возможности
        drv = driver_path or os.environ.get("YA_DRIVER")
        if drv and Path(drv).exists():
            service = ChromeService(executable_path=drv)
            return webdriver.Chrome(service=service, options=options)
        # Фоллбэк — пусть Selenium Manager попробует сам
        return webdriver.Chrome(options=options)

    # Chrome по умолчанию (Selenium Manager подтянет chromedriver)
    return webdriver.Chrome(options=options)


def login_once(driver: webdriver.Chrome, email: str, password: str, timeout: int = 30) -> None:
    driver.get(BASE_URL)

    # Кликнуть "Личный кабинет"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(L.BTN_ACCOUNT)).click()

    # Ввести логин/пароль
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(L.INPUT_EMAIL)).send_keys(email)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(L.INPUT_PASSWORD)).send_keys(password)

    # Нажать "Войти"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(L.BTN_LOGIN)).click()

    # Подтверждение авторизации — ждём, что кнопка "Войти" исчезнет
    WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(L.BTN_LOGIN))


def fetch_product(driver: webdriver.Chrome, url: str, timeout: int = 30) -> tuple[str, int, str]:
    driver.get(url)

    # Название
    title_elt = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(L.PRODUCT_TITLE))
    name = title_elt.text.strip()

    # Цена + валюта
    value_elt = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(L.PRICE_VALUE))
    curr_elt = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(L.PRICE_CURRENCY))
    price_minor, currency = parse_price_and_currency(value_elt.text, curr_elt.text)
    return name, price_minor, currency


def cmd_init_db(_: argparse.Namespace) -> None:
    db.init_db()
    print(f"Инициализация БД: {db.DB_PATH.resolve()}")


def cmd_fetch(args: argparse.Namespace) -> None:
    db.init_db()

    # Секреты
    secrets = load_env_kv(Path(args.secrets))
    email = secrets.get("email") or secrets.get("user") or secrets.get("login")
    password = secrets.get("password")
    if not email or not password:
        print(f"В {args.secrets} должны быть строки вида:\nemail=you@example.com\npassword=SECRET")
        return

    # Ссылки
    groups = load_links_txt(Path(args.links))
    if not groups:
        print("Файл со ссылками пуст. Заполните links_perfumex.txt (1 строка = 1 товар, фоллбэки через '|').")
        return

    driver = build_driver(browser=args.browser, headless=not args.headful, driver_path=args.driver_path)
    try:
        print("→ Авторизация на сайте…")
        login_once(driver, email, password, timeout=30)
        print("   Авторизация успешна.")

        # Обход карточек
        for urls in groups:
            last_error = None
            fetched = False
            for url in urls:
                print(f"   Пробую: {url}")
                try:
                    name, price_minor, currency = fetch_product(driver, url, timeout=30)
                    pid = db.upsert_product(name)
                    latest_latest = db.insert_price(pid, price_minor, currency)
                    # получим предыдущее значение для сообщения пользователю
                    # (лучше не делать отдельный запрос — но для краткости оставим так)
                    print(f"   ОК: {name} — {price_minor/100:.2f} {currency}")
                    fetched = True
                    break
                except Exception as e:
                    last_error = e
                    print(f"   Ошибка: {e}")
            if not fetched:
                print(f"   Не удалось получить цену ни по одному URL. Последняя ошибка: {last_error}")

    finally:
        driver.quit()


def cmd_report(args: argparse.Namespace) -> None:
    from perfumex_report import build_excel_report
    out_path = Path(args.output)
    try:
        out_path = build_excel_report(out_path)
        print(f"Отчёт сформирован: {out_path.resolve()}")
    except PermissionError:
        print("Не удалось записать отчёт. Похоже, файл открыт в Excel/Numbers. Закройте и повторите.")


def main():
    parser = argparse.ArgumentParser(description="Perfumex price tracker")
    sub = parser.add_subparsers(required=True)

    p1 = sub.add_parser("init-db", help="Создать/инициализировать БД perfumex")
    p1.set_defaults(func=cmd_init_db)

    p2 = sub.add_parser("fetch", help="Собрать данные (авторизация + карточки)")
    p2.add_argument("--links", default=str(DEFAULT_LINKS_FILE), help="Файл со ссылками (links_perfumex.txt)")
    p2.add_argument("--secrets", default=str(DEFAULT_SECRETS_FILE), help="Файл с логином/паролем (secrets_perfumex.env)")
    p2.add_argument("--browser", default="chrome", choices=["chrome", "yandex"], help="Браузер: chrome или yandex")
    p2.add_argument("--headful", action="store_true", help="Окно браузера (по умолчанию headless)")
    p2.add_argument("--driver-path", default=None, help="Путь к yandexdriver (для --browser yandex)")
    p2.set_defaults(func=cmd_fetch)

    p3 = sub.add_parser("report", help="Сформировать Excel-отчёт perfumex")
    p3.add_argument("--output", default="perfumex_report.xlsx", help="Путь к .xlsx")
    p3.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
