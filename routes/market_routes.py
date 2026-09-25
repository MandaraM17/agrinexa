from flask import Blueprint, request
from models import db


market_bp = Blueprint("market", __name__)


market_prices = [
    {
        "id": 1,
        "crop": "Arecanut",
        "market": "Mangalore",
        "price": 35000,
        "unit": "per quintal"
    },
    {
        "id": 2,
        "crop": "Paddy",
        "market": "Udupi",
        "price": 2800,
        "unit": "per quintal"
    },
    {
        "id": 3,
        "crop": "Coconut",
        "market": "Mangalore",
        "price": 3200,
        "unit": "per 100 nuts"
    }
]


@market_bp.route("/", methods=["GET"])
def market_home():
    return {
        "message": "Market Price API is working!"
    }


@market_bp.route("/prices", methods=["GET"])
def get_market_prices():
    return {
        "prices": market_prices
    }


@market_bp.route("/<string:crop_name>", methods=["GET"])
def get_crop_price(crop_name):

    for item in market_prices:
        if item["crop"].lower() == crop_name.lower():
            return item

    return {
        "error": "Crop price not found"
    }, 404