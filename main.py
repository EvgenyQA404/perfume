import argparse
import json
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import db
import locators
from utils import parse_rub

DEFAULT_URLS_FILE = Path("urls.json")
DEFAULT_LINKS_FILE = Path("links.txt")


def load_urls_json(urls_file: Path):
    if not urls_file.exists():
        try:
            import data
            legacy = [getattr(data, "url", None), getattr(data, "url_two", None)]
            return [u for u in legacy if u]
        except Exception:
            return []
    return json.loads(urls_file.read_text(encoding="utf-8"))


def load_links_txt(links_file: Path):
    """
    Формат:
      • ОДНА строка = ОДИН товар.
      • Пустые строки и строки, начинающиеся с '#', игнорируются.
      • Фоллбэки для ОДНОГО товара — в одной строке через '|'.
    Возвращает: List[List[str]] — каждая строка -> список fallback-URL'ов.
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


def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


def fetch_once(url: str, timeout: int = 30) -> tuple[str, int]:
    driver = build_driver(headless=True)
    driver.get(url)
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locators.product))
        name = driver.find_element(*locators.product).text.strip()
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locators.price))
        price_text = driver.find_element(*locators.price).text.strip()
        price_val = parse_rub(price_text)
        if price_val is None:
            raise ValueError(f"Не удалось распарсить цену: '{price_text}'")
        return name, price_val
    finally:
        driver.quit()


def cmd_init_db(_: argparse.Namespace) -> None:
    db.init_db()
    print(f"Инициализация БД: {db.DB_PATH.resolve()}")


def _iterate_entries_from_json(cfg_json):
    entries = []
    if isinstance(cfg_json, list) and cfg_json and isinstance(cfg_json[0], dict):
        for item in cfg_json:
            name = item.get("name")
            urls = [u for u in (item.get("urls") or []) if u]
            if urls:
                entries.append((name, urls))
    else:
        urls = [u for u in (cfg_json or []) if u]
        for u in urls:
            entries.append((None, [u]))
    return entries


def _iterate_entries_from_links(groups):
    entries = []
    for g in groups:
        urls = [u for u in g if u]
        if urls:
            entries.append((None, urls))
    return entries


def cmd_fetch(args: argparse.Namespace) -> None:
    db.init_db()

    if args.links:
        entries = _iterate_entries_from_links(load_links_txt(Path(args.links)))
    else:
        entries = _iterate_entries_from_json(load_urls_json(Path(args.urls)))

    if not entries:
        print("Список ссылок пуст. Добавьте их в links.txt или urls.json (или data.url*).")
        return

    for conf_name, urls in entries:
        title = conf_name or "auto (name со страницы)"
        print(f"→ Обрабатываю группу: {title}")
        last_error = None
        fetched = False
        for url in urls:
            print(f"   Пробую URL: {url}")
            try:
                scraped_name, price_val = fetch_once(url)
                pid = db.upsert_product(scraped_name)  # уникальность по имени товара
                latest, prev = db.latest_and_previous_price(pid)
                db.insert_price(pid, price_val)
                print(f"   ОК: {scraped_name} — {price_val} ₽ (предыдущее: {prev if prev is not None else '—'})")
                fetched = True
                break  # первый удачный URL из фоллбэков
            except Exception as e:
                last_error = e
                print(f"   Ошибка: {e}")
        if not fetched:
            print(f"   Не удалось получить цену ни по одному URL. Последняя ошибка: {last_error}")


def cmd_report(args: argparse.Namespace) -> None:
    from report import build_excel_report
    out_path = Path(args.output)
    try:
        out_path = build_excel_report(out_path)
        print(f"Отчёт сформирован: {out_path.resolve()}")
    except PermissionError:
        print(
            "Не удалось записать файл отчёта. Похоже, он сейчас открыт в Excel.\n"
            "Пожалуйста, закройте файл 'price_report.xlsx' и запустите команду снова."
        )


def main():
    parser = argparse.ArgumentParser(description="Price tracker: fetch & report")
    sub = parser.add_subparsers(required=True)

    p1 = sub.add_parser("init-db", help="Создать/инициализировать БД")
    p1.set_defaults(func=cmd_init_db)

    p2 = sub.add_parser("fetch", help="Собрать данные (скрапинг) и записать в БД")
    p2.add_argument("--urls", default=str(DEFAULT_URLS_FILE), help="Файл со списком URL (urls.json)")
    p2.add_argument("--links", default=None, help="Простой текстовый файл со ссылками (links.txt)")
    p2.set_defaults(func=cmd_fetch)

    p3 = sub.add_parser("report", help="Сформировать Excel отчёт в корне проекта")
    p3.add_argument("--output", default="price_report.xlsx", help="Путь к файлу отчёта .xlsx")
    p3.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
