import copy
from unittest.mock import patch
import pytest
import app as app_module

START_DATA = copy.deepcopy(app_module.inventory)

@pytest.fixture
def client():
    app_module.inventory.clear()
    app_module.inventory.extend(copy.deepcopy(START_DATA))
    return app_module.app.test_client()

def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_one_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Organic Almond Milk"


def test_get_item_not_found(client):
    assert client.get("/inventory/99").status_code == 404


def test_add_item(client):
    new_item = {"product_name": "Rice", "price": 2.5, "stock": 10}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    assert response.get_json()["id"] == 3
    assert len(client.get("/inventory").get_json()) == 3


def test_add_item_missing_price(client):
    response = client.post("/inventory", json={"product_name": "Rice"})
    assert response.status_code == 400


def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 9.99, "stock": 5})
    assert response.status_code == 200
    assert response.get_json()["price"] == 9.99
    assert response.get_json()["stock"] == 5


def test_update_item_not_found(client):
    assert client.patch("/inventory/99", json={"price": 1}).status_code == 404


def test_delete_item(client):
    assert client.delete("/inventory/1").status_code == 200
    assert client.get("/inventory/1").status_code == 404


def test_delete_item_not_found(client):
    assert client.delete("/inventory/99").status_code == 404

FAKE_PRODUCT = {"product_name": "Nutella", "brands": "Ferrero",
                "ingredients_text": "Sugar, palm oil, hazelnuts"}

@patch("app.get_product_by_barcode", return_value=FAKE_PRODUCT)
def test_lookup_by_barcode(mock_api, client):
    response = client.get("/lookup?barcode=123")
    assert response.status_code == 200
    assert response.get_json()["brands"] == "Ferrero"

@patch("app.get_product_by_name", return_value=FAKE_PRODUCT)
def test_lookup_by_name(mock_api, client):
    response = client.get("/lookup?name=nutella")
    assert response.status_code == 200

@patch("app.get_product_by_barcode", return_value=None)
def test_lookup_not_found(mock_api, client):
    assert client.get("/lookup?barcode=000").status_code == 404

def test_lookup_without_params(client):
    assert client.get("/lookup").status_code == 400

@patch("app.get_product_by_barcode", return_value=FAKE_PRODUCT)
def test_add_item_with_barcode_gets_extra_details(mock_api, client):
    new_item = {"product_name": "Nutella", "price": 5, "barcode": "123"}
    response = client.post("/inventory", json=new_item)
    assert response.get_json()["brands"] == "Ferrero"

