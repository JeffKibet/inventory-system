from flask import Flask, jsonify, request
import requests

from off_client import get_product_by_barcode, get_product_by_name

app = Flask(__name__)

inventory = [
    {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk",
     "ingredients_text": "Filtered water, almonds, cane sugar",
     "barcode": "0025293001442", "price": 4.99, "stock": 20},
    {"id": 2, "product_name": "Peanut Butter", "brands": "Jif",
     "ingredients_text": "Roasted peanuts, sugar, salt",
     "barcode": "0051500240144", "price": 3.49, "stock": 35},
]

def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_one_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)
    if not data or "product_name" not in data or "price" not in data:
        return jsonify({"error": "product_name and price are required"}), 400

    if inventory:
        new_id = inventory[-1]["id"] + 1
    else:
        new_id = 1

    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brands": data.get("brands", "Unknown"),
        "ingredients_text": data.get("ingredients_text", ""),
        "barcode": data.get("barcode", ""),
        "price": data["price"],
        "stock": data.get("stock", 0),
    }

    if new_item["barcode"]:
        try:
            product = get_product_by_barcode(new_item["barcode"])
            if product:
                new_item["brands"] = product["brands"]
                new_item["ingredients_text"] = product["ingredients_text"]
        except requests.RequestException:
            pass  

    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data sent"}), 400

    for field in ["product_name", "brands", "price", "stock"]:
        if field in data:
            item[field] = data[field]
    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200

@app.route("/lookup", methods=["GET"])
def lookup():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    try:
        if barcode:
            product = get_product_by_barcode(barcode)
        elif name:
            product = get_product_by_name(name)
        else:
            return jsonify({"error": "Give a barcode or a name"}), 400
    except requests.RequestException:
        return jsonify({"error": "OpenFoodFacts API failed"}), 502

    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)