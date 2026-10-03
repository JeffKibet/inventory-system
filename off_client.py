import requests

BASE_URL = "https://world.openfoodfacts.org"

def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/api/v0/product/{barcode}.json"
    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("status") != 1:
        return None

    product = data["product"]
    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
    }

def get_product_by_name(name):
    """Search OpenFoodFacts by name and return the first match, or None."""
    url = f"{BASE_URL}/cgi/search.pl"
    params = {"search_terms": name, "search_simple": 1,
              "action": "process", "json": 1, "page_size": 1}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if not data.get("products"):
        return None

    product = data["products"][0]
    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
    }
