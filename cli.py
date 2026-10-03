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

def view_one():
    item_id = input("Item ID: ")
    try:
        response = requests.get(f"{API_URL}/inventory/{item_id}")
    except requests.RequestException:
        print("Cannot reach the API. Is app.py running?")
        return
    if response.status_code == 200:
        show_item(response.json())
    else:
        print(response.json()["error"])

def add_item():
    name = input("Product name: ")
    barcode = input("Barcode (press Enter to skip): ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Price and stock must be numbers.")
        return

    new_item = {"product_name": name, "price": price,
                "stock": stock, "barcode": barcode}
    try:
        response = requests.post(f"{API_URL}/inventory", json=new_item)
    except requests.RequestException:
        print("Cannot reach the API. Is app.py running?")
        return
    if response.status_code == 201:
        print("Item added!")
        show_item(response.json())
    else:
        print(response.json()["error"])