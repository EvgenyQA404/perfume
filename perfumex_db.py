# perfumex_db.py — SQLite для perfumex.ru (уникальность по имени)

import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List

DB_PATH = Path("perfumex.sqlite3")

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price_minor INTEGER NOT NULL, -- цена в минимальных единицах (центы)
    currency TEXT NOT NULL,       -- 'USD', 'RUB', ...
    checked_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE INDEX IF NOT EXISTS idx_prices_product_time ON prices(product_id, checked_at);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db() -> None:
    conn = get_conn()
    with conn:
        conn.executescript(SCHEMA_SQL)
    conn.close()


def upsert_product(name: str) -> int:
    conn = get_conn()
    with conn:
        cur = conn.execute(
            "INSERT INTO products(name) VALUES(?) "
            "ON CONFLICT(name) DO UPDATE SET name=excluded.name "
            "RETURNING id",
            (name,),
        )
        row = cur.fetchone()
    conn.close()
    return int(row[0])


def insert_price(product_id: int, price_minor: int, currency: str) -> None:
    conn = get_conn()
    with conn:
        conn.execute(
            "INSERT INTO prices(product_id, price_minor, currency) VALUES(?,?,?)",
            (product_id, price_minor, currency),
        )
    conn.close()


def dump_history() -> List[tuple]:
    """
    Возвращает полную историю: (product_id, name, price_minor, currency, checked_at)
    """
    conn = get_conn()
    cur = conn.execute(
        """
        SELECT p.id, p.name, pr.price_minor, pr.currency, pr.checked_at
        FROM prices pr
        JOIN products p ON p.id = pr.product_id
        ORDER BY p.name, pr.checked_at
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows
