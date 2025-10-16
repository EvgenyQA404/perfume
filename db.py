import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List

DB_PATH = Path("price_tracker.sqlite3")

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
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
            "INSERT INTO products(name) VALUES(?) ON CONFLICT(name) DO UPDATE SET name=excluded.name RETURNING id",
            (name,)
        )
        row = cur.fetchone()
    conn.close()
    return int(row[0])


def insert_price(product_id: int, price: int) -> None:
    conn = get_conn()
    with conn:
        conn.execute("INSERT INTO prices(product_id, price) VALUES(?, ?)", (product_id, price))
    conn.close()


def latest_and_previous_price(product_id: int) -> Tuple[Optional[int], Optional[int]]:
    conn = get_conn()
    cur = conn.execute(
        "SELECT price FROM prices WHERE product_id=? ORDER BY checked_at DESC LIMIT 2",
        (product_id,),
    )
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    if not rows:
        return None, None
    if len(rows) == 1:
        return rows[0], None
    return rows[0], rows[1]


def dump_history() -> List[tuple]:
    conn = get_conn()
    cur = conn.execute(
        """
        SELECT p.id, p.name, pr.price, pr.checked_at
        FROM prices pr
        JOIN products p ON p.id = pr.product_id
        ORDER BY p.name, pr.checked_at
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows