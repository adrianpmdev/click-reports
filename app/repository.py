"""
Repository

Data access layer for products and clicks. Keeps every SQL query in one
place; filters and aggregations run in SQL, not in memory.

@author adrianpmdev
"""

import sqlite3
from datetime import datetime, timezone


def product_exists(connection: sqlite3.Connection, product_id: int) -> bool:
    row = connection.execute("SELECT 1 FROM products WHERE id = ?", (product_id,)).fetchone()
    return row is not None


def create_click(connection: sqlite3.Connection, product_id: int) -> dict:
    clicked_at = datetime.now(timezone.utc).isoformat()
    cursor = connection.execute(
        "INSERT INTO clicks (product_id, clicked_at) VALUES (?, ?)",
        (product_id, clicked_at),
    )
    connection.commit()
    return {"id": cursor.lastrowid, "product_id": product_id, "clicked_at": clicked_at}


def count_clicks_by_product(connection: sqlite3.Connection) -> list[dict]:
    """Total clicks per product, including products without clicks, most clicked first."""
    rows = connection.execute(
        """
        SELECT p.id AS product_id, p.name, COUNT(c.id) AS total_clicks
        FROM products p
        LEFT JOIN clicks c ON c.product_id = p.id
        GROUP BY p.id
        ORDER BY total_clicks DESC, p.id
        """
    ).fetchall()
    return [dict(row) for row in rows]


def count_clicks_by_day(connection: sqlite3.Connection, product_id: int | None) -> list[dict]:
    """Total clicks per UTC day, optionally only for one product, oldest day first."""
    rows = connection.execute(
        """
        SELECT date(clicked_at) AS date, COUNT(*) AS total_clicks
        FROM clicks
        WHERE ?1 IS NULL OR product_id = ?1
        GROUP BY date(clicked_at)
        ORDER BY date
        """,
        (product_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def count_clicks_by_day_and_product(connection: sqlite3.Connection) -> list[dict]:
    """Clicks per UTC day and product, ordered by day and product."""
    rows = connection.execute(
        """
        SELECT date(c.clicked_at) AS date, c.product_id, p.name AS product, COUNT(*) AS clicks
        FROM clicks c
        JOIN products p ON p.id = c.product_id
        GROUP BY date(c.clicked_at), c.product_id
        ORDER BY date, c.product_id
        """
    ).fetchall()
    return [dict(row) for row in rows]
