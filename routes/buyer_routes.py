from flask import Blueprint, request, jsonify
from models import db, Buyer

buyer_bp = Blueprint("buyer", __name__)


# --------------------------------------------------
# REGISTER BUYER
# POST /api/buyers/register
# --------------------------------------------------
@buyer_bp.route("/register", methods=["POST"])
def register_buyer():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    name = data.get("name")
    location = data.get("location")
    crop = data.get("crop")
    phone = data.get("phone")
    price_per_kg = data.get("price_per_kg")

    if not name or not location or not crop or not phone or price_per_kg is None:
        return jsonify({
            "success": False,
            "message": "Name, location, crop, phone and price per kg are required"
        }), 400

    buyer = Buyer(
        name=name,
        village=location,
        crop=crop,
        phone=phone,
        price_per_kg=price_per_kg
    )

    db.session.add(buyer)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Buyer registered successfully",
        "buyer": {
            "id": buyer.id,
            "name": buyer.name,
            "location": buyer.village,
            "crop": buyer.crop,
            "phone": buyer.phone,
            "price_per_kg": buyer.price_per_kg
        }
    }), 201


# --------------------------------------------------
# GET ALL BUYERS
# GET /api/buyers/all
# --------------------------------------------------
@buyer_bp.route("/all", methods=["GET"])
def get_all_buyers():

    buyers = Buyer.query.all()

    buyer_list = []

    for buyer in buyers:
        buyer_list.append({
            "id": buyer.id,
            "name": buyer.name,
            "location": buyer.village,
            "crop": buyer.crop,
            "phone": buyer.phone,
            "price_per_kg": buyer.price_per_kg
        })

    return jsonify({
        "success": True,
        "buyers": buyer_list
    }), 200


# --------------------------------------------------
# GET BUYER BY ID
# GET /api/buyers/<id>
# --------------------------------------------------
@buyer_bp.route("/<int:buyer_id>", methods=["GET"])
def get_buyer(buyer_id):

    buyer = Buyer.query.get(buyer_id)

    if not buyer:
        return jsonify({
            "success": False,
            "message": "Buyer not found"
        }), 404

    return jsonify({
        "success": True,
        "buyer": {
            "id": buyer.id,
            "name": buyer.name,
            "location": buyer.village,
            "crop": buyer.crop,
            "phone": buyer.phone,
            "price_per_kg": buyer.price_per_kg
        }
    }), 200