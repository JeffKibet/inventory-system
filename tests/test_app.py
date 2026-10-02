import copy
from unittest.mock import patch
 
import pytest
 
import app as app_module
import off_client
 
ORIGINAL = copy.deepcopy(app_module.inventory)

@pytest.fixture
def client():
    # Reset the mock database before every test
    app_module.inventory[:] = copy.deepcopy(ORIGINAL)
    app_module.id_counter = 2
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()

def test_get_all(client):
    res = client.get("/inventory")
    assert res.status_code == 200
    assert len(res.get_json()) == 2

def test_get_one(client):
    res = client.get("/inventory/1")
    assert res.status_code == 200
    assert res.get_json()["product_name"] == "Organic Almond Milk"

def test_get_one_not_found(client):
    assert client.get("/inventory/999").status_code == 404
 