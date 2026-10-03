from flask import Flask, jsonify, request
import requests

from off_client import get_product_by_barcode, get_product_by_name

app = Flask(__name__)
