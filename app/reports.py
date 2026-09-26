"""
Reports

Click statistics built with Pandas: totals per product, totals per day and
the CSV export (clicks per day and product).

@author adrianpmdev
"""

import sqlite3

import pandas as pd

CLICKS_QUERY = """
SELECT c.product_id, p.name, c.clicked_at
FROM clicks c
JOIN products p ON p.id = c.product_id
"""


def load_clicks(connection: sqlite3.Connection) -> pd.DataFrame:
    """Loads every click with its product name and a `date` column."""
    df = pd.read_sql_query(CLICKS_QUERY, connection)
    df["date"] = pd.to_datetime(df["clicked_at"], utc=True, format="ISO8601").dt.date
    return df


def clicks_by_product(connection: sqlite3.Connection) -> list[dict]:
    """Total clicks per product, including products without clicks."""
    products = pd.read_sql_query("SELECT id AS product_id, name FROM products", connection)
    totals = load_clicks(connection).groupby("product_id").size().rename("total_clicks")
    result = products.join(totals, on="product_id").fillna({"total_clicks": 0})
    result["total_clicks"] = result["total_clicks"].astype(int)
    return result.sort_values("total_clicks", ascending=False).to_dict(orient="records")


def clicks_by_day(connection: sqlite3.Connection, product_id: int | None = None) -> list[dict]:
    """Total clicks per day, optionally filtered by product."""
    df = load_clicks(connection)
    if product_id is not None:
        df = df[df["product_id"] == product_id]
    daily = df.groupby("date").size().reset_index(name="total_clicks")
    return daily.sort_values("date").to_dict(orient="records")


def clicks_report_csv(connection: sqlite3.Connection) -> str:
    """CSV with one row per day and product: date, product_id, product, clicks."""
    df = load_clicks(connection)
    report = (
        df.groupby(["date", "product_id", "name"])
        .size()
        .reset_index(name="clicks")
        .rename(columns={"name": "product"})
        .sort_values(["date", "product_id"])
    )
    return report.to_csv(index=False)
