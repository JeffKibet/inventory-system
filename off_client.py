import requests

BASE_URL = "https://world.openfoodfacts.org"

def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/api/v0/product/{barcode}.json"
    response = requests.get(url, timeout=10)
    data = response.json()

    