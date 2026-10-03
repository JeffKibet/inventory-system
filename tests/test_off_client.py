from unittest.mock import MagicMock, patch

import off_client

@patch("off_client.requests.get")
def test_get_product_by_barcode_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Organic Almond Milk", "brands": "Silk",
                    "ingredients_text": "Filtered water, almonds"},
    }
    mock_get.return_value = mock_response

    result = off_client.get_product_by_barcode("123")
    assert result["product_name"] == "Organic Almond Milk"
    assert result["brands"] == "Silk"


@patch("off_client.requests.get")
def test_get_product_by_barcode_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    mock_get.return_value = mock_response

    assert off_client.get_product_by_barcode("000") is None


@patch("off_client.requests.get")
def test_get_product_by_name_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [{"product_name": "Nutella", "brands": "Ferrero"}]
    }
    mock_get.return_value = mock_response

    assert off_client.get_product_by_name("nutella")["brands"] == "Ferrero"


@patch("off_client.requests.get")
def test_get_product_by_name_no_results(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"products": []}
    mock_get.return_value = mock_response

    assert off_client.get_product_by_name("zzzz") is None