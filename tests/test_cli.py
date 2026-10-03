from unittest.mock import MagicMock, patch

import cli

def fake_response(status_code, data):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = data
    return response


@patch("cli.requests.delete")
@patch("builtins.input", return_value="1")
def test_delete_item(mock_input, mock_delete, capsys):
    mock_delete.return_value = fake_response(200, {"message": "Item deleted"})
    cli.delete_item()
    assert "Item deleted" in capsys.readouterr().out


@patch("cli.requests.get")
@patch("builtins.input", return_value="99")
def test_view_one_not_found(mock_input, mock_get, capsys):
    mock_get.return_value = fake_response(404, {"error": "Item not found"})
    cli.view_one()
    assert "Item not found" in capsys.readouterr().out


@patch("builtins.input", side_effect=["Rice", "", "abc"])
def test_add_item_rejects_bad_price(mock_input, capsys):
    cli.add_item()
    assert "must be numbers" in capsys.readouterr().out


@patch("cli.requests.post")
@patch("builtins.input", side_effect=["Rice", "", "2.5", "10"])
def test_add_item_sends_data(mock_input, mock_post, capsys):
    item = {"id": 3, "product_name": "Rice", "brands": "Unknown",
            "price": 2.5, "stock": 10}
    mock_post.return_value = fake_response(201, item)
    cli.add_item()
    assert "Item added" in capsys.readouterr().out


@patch("builtins.input", side_effect=["9", "0"])
def test_menu_invalid_choice_then_quit(mock_input, capsys):
    cli.main()
    output = capsys.readouterr().out
    assert "Invalid choice" in output
    assert "Goodbye" in output