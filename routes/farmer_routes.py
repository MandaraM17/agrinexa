from flask import Blueprint, request
from models import db, Farmer

farmer_bp = Blueprint("farmer", __name__)


@farmer_bp.route("/", methods=["GET"])
def farmer_home():
    return {
        "message": "Farmer API is working!"
    }


@farmer_bp.route("/register", methods=["POST"])
def register_farmer():
    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    village = data.get("village")

    if not name or not phone or not village:
        return {
            "error": "Name, phone and village are required"
        }, 400

    farmer = Farmer(
        name=name,
        phone=phone,
        village=village
    )

    db.session.add(farmer)
    db.session.commit()

    return {
        "message": "Farmer registered successfully!",
        "farmer_id": farmer.id
    }, 201


@farmer_bp.route("/all", methods=["GET"])
def get_all_farmers():
    farmers = Farmer.query.all()

    farmer_list = []

    for farmer in farmers:
        farmer_list.append({
            "id": farmer.id,
            "name": farmer.name,
            "phone": farmer.phone,
            "village": farmer.village
        })

    return {
        "farmers": farmer_list
    }