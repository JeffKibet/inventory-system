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