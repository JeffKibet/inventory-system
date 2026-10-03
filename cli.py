import requests

API_URL = "http://127.0.0.1:5000"

def show_item(item):
    print(f"[{item['id']}] {item['product_name']} - {item['brands']}")
    print(f"    Price: {item['price']} | Stock: {item['stock']}")


def view_all():
    try:
        response = requests.get(f"{API_URL}/inventory")
    except requests.RequestException:
        print("Cannot reach the API. Is app.py running?")
        return
    for item in response.json():
        show_item(item)