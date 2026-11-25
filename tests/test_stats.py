"""
Stats tests

Tests of the click statistics and the CSV report with a small known dataset.

@author adrianpmdev
"""

import pytest

PRODUCTS = ["Lamp", "Chair", "Table"]
CLICKS = [
    (1, "2026-09-01T10:00:00+00:00"),
    (1, "2026-09-01T23:59:00+00:00"),
    (2, "2026-09-01T12:00:00+00:00"),
    (1, "2026-09-02T00:30:00+00:00"),
]


@pytest.fixture
def known_data(insert_data):
    insert_data(PRODUCTS, CLICKS)


def test_clicks_by_product_includes_products_without_clicks_most_clicked_first(client, known_data):
    response = client.get("/stats/products")

    assert response.status_code == 200
    assert response.json() == [
        {"product_id": 1, "name": "Lamp", "total_clicks": 3},
        {"product_id": 2, "name": "Chair", "total_clicks": 1},
        {"product_id": 3, "name": "Table", "total_clicks": 0},
    ]


def test_clicks_by_day_can_be_filtered_by_product(client, known_data):
    response = client.get("/stats/daily", params={"product_id": 2})

    assert response.json() == [{"date": "2026-09-01", "total_clicks": 1}]


def test_csv_report_has_one_row_per_day_and_product(client, known_data):
    response = client.get("/reports/clicks.csv")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert response.text.splitlines() == [
        "date,product_id,product,clicks",
        "2026-09-01,1,Lamp,2",
        "2026-09-01,2,Chair,1",
        "2026-09-02,1,Lamp,1",
    ]
