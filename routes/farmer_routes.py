from flask import Blueprint, request, jsonify
from models import db, Farmer

farmer_bp = Blueprint("farmer", __name__)


# --------------------------------------------------
# REGISTER FARMER
# POST /api/farmers/register
# --------------------------------------------------
@farmer_bp.route("/register", methods=["POST"])
def register_farmer():

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

    if not name or not location or not crop or not phone:
        return jsonify({
            "success": False,
            "message": "Name, location, crop and phone are required"
        }), 400

    farmer = Farmer(
        name=name,
        village=location,
        crop=crop,
        phone=phone
    )

    db.session.add(farmer)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Farmer registered successfully",
        "farmer": {
            "id": farmer.id,
            "name": farmer.name,
            "location": farmer.village,
            "crop": farmer.crop,
            "phone": farmer.phone
        }
    }), 201


# --------------------------------------------------
# GET ALL FARMERS
# GET /api/farmers/all
# --------------------------------------------------
@farmer_bp.route("/all", methods=["GET"])
def get_all_farmers():

    farmers = Farmer.query.all()

    farmer_list = []

    for farmer in farmers:
        farmer_list.append({
            "id": farmer.id,
            "name": farmer.name,
            "location": farmer.village,
            "crop": farmer.crop,
            "phone": farmer.phone
        })

    return jsonify({
        "success": True,
        "farmers": farmer_list
    }), 200


# --------------------------------------------------
# GET FARMER BY ID
# GET /api/farmers/<id>
# --------------------------------------------------
@farmer_bp.route("/<int:farmer_id>", methods=["GET"])
def get_farmer(farmer_id):

    farmer = Farmer.query.get(farmer_id)

    if not farmer:
        return jsonify({
            "success": False,
            "message": "Farmer not found"
        }), 404

    return jsonify({
        "success": True,
        "farmer": {
            "id": farmer.id,
            "name": farmer.name,
            "location": farmer.village,
            "crop": farmer.crop,
            "phone": farmer.phone
        }
    }), 200