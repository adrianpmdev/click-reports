"""
Clicks tests

Tests of the health check and the endpoint that registers clicks.

@author adrianpmdev
"""


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_registering_a_click_returns_201_and_the_click(client, insert_data):
    insert_data(["Lamp"])

    response = client.post("/clicks", json={"product_id": 1})

    assert response.status_code == 201
    click = response.json()
    assert click["product_id"] == 1
    assert click["clicked_at"] is not None


def test_registering_a_click_on_a_missing_product_returns_404(client):
    response = client.post("/clicks", json={"product_id": 99})

    assert response.status_code == 404
