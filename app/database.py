"""
Database

SQLite connection handling, schema creation and sample data seeding.

@author adrianpmdev
"""

import random
import sqlite3
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone

from app.config import DB_PATH, SAMPLE_CLICKS, SAMPLE_DAYS

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clicks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products (id),
    clicked_at TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clicks_product ON clicks (product_id);
CREATE INDEX IF NOT EXISTS idx_clicks_date ON clicks (clicked_at);
"""

SAMPLE_PRODUCTS = [
    "Wireless headphones",
    "Mechanical keyboard",
    "Gaming mouse",
    "USB-C hub",
    "Webcam HD",
]


def get_connection() -> sqlite3.Connection:
    """Opens a new SQLite connection that returns rows as dict-like objects."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: one connection per request, always closed."""
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


def _random_clicks(product_ids: list[int]) -> list[tuple[int, str]]:
    """Generates clicks spread over the last SAMPLE_DAYS days."""
    rng = random.Random(42)  # Fixed seed: same sample data on every fresh start.
    now = datetime.now(timezone.utc)
    weights = [5, 3, 4, 1, 2][: len(product_ids)]
    clicks = []
    for _ in range(SAMPLE_CLICKS):
        product_id = rng.choices(product_ids, weights=weights)[0]
        clicked_at = now - timedelta(minutes=rng.randint(0, SAMPLE_DAYS * 24 * 60))
        clicks.append((product_id, clicked_at.isoformat()))
    return clicks


def init_db() -> None:
    """Creates the schema and inserts sample data if the database is empty."""
    connection = get_connection()
    try:
        connection.executescript(SCHEMA)
        count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO products (name) VALUES (?)",
                [(name,) for name in SAMPLE_PRODUCTS],
            )
            product_ids = [row[0] for row in connection.execute("SELECT id FROM products")]
            connection.executemany(
                "INSERT INTO clicks (product_id, clicked_at) VALUES (?, ?)",
                _random_clicks(product_ids),
            )
            connection.commit()
    finally:
        connection.close()
