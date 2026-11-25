"""
Reports

CSV export of the clicks per day and product, built with Pandas from the
totals already aggregated in SQL.

@author adrianpmdev
"""

import sqlite3

import pandas as pd

from app import repository

CSV_COLUMNS = ["date", "product_id", "product", "clicks"]


def clicks_report_csv(connection: sqlite3.Connection) -> str:
    """CSV with one row per day and product: date, product_id, product, clicks."""
    rows = repository.count_clicks_by_day_and_product(connection)
    return pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(index=False)
