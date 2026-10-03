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