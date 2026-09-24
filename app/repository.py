"""
Repository

Data access layer for products and clicks.

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
