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

def update_item():
    item_id = input("Item ID: ")
    try:
        price = float(input("New price: "))
        stock = int(input("New stock: "))
    except ValueError:
        print("Price and stock must be numbers.")
        return
    try:
        response = requests.patch(f"{API_URL}/inventory/{item_id}",
                                  json={"price": price, "stock": stock})
    except requests.RequestException:
        print("Cannot reach the API. Is app.py running?")
        return
    if response.status_code == 200:
        print("Item updated!")
        show_item(response.json())
    else:
        print(response.json()["error"])

def delete_item():
    item_id = input("Item ID: ")
    try:
        response = requests.delete(f"{API_URL}/inventory/{item_id}")
    except requests.RequestException:
        print("Cannot reach the API. Is app.py running?")
        return
    if response.status_code == 200:
        print("Item deleted!")
    else:
        print(response.json()["error"])

def find_on_api():
    choice = input("Search by 1) barcode or 2) name: ")
    if choice == "1":
        params = {"barcode": input("Barcode: ")}
    elif choice == "2":
        params = {"name": input("Name: ")}
    else:
        print("Invalid choice.")
        return
    try:
        response = requests.get(f"{API_URL}/lookup", params=params)
    except requests.RequestException:
        print("Cannot reach the API. Is app.py running?")
        return
    if response.status_code == 200:
        product = response.json()
        print(product["product_name"], "-", product["brands"])
        print("Ingredients:", product["ingredients_text"])
    else:
        print(response.json()["error"])


def main():
    while True:
        print("\n--- Inventory Manager ---")
        print("1. View all items")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Find product on OpenFoodFacts")
        print("0. Quit")
        choice = input("Choose: ")

        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            find_on_api()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
