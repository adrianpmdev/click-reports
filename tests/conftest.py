"""
Conftest

Test fixtures: a temporary empty database, helpers to insert known data and
a test client.

@author adrianpmdev
"""

from collections.abc import Sequence

import pytest
from fastapi.testclient import TestClient

from app import config
from app.database import get_connection, init_db
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setattr(config, "SEED_SAMPLE_DATA", False)
    init_db()
    return TestClient(app)


@pytest.fixture
def insert_data(client):
    """Inserts products by name and clicks as (product_id, clicked_at) pairs."""

    def insert(products: list[str], clicks: Sequence[tuple[int, str]] = ()) -> None:
        connection = get_connection()
        try:
            connection.executemany(
                "INSERT INTO products (name) VALUES (?)", [(name,) for name in products]
            )
            connection.executemany(
                "INSERT INTO clicks (product_id, clicked_at) VALUES (?, ?)", clicks
            )
            connection.commit()
        finally:
            connection.close()

    return insert
