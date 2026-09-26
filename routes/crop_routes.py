from flask import Blueprint, request, jsonify
from models import db, Crop

crop_bp = Blueprint("crop", __name__)


# --------------------------------------------------
# ADD CROP
# POST /api/crops/register
# --------------------------------------------------
@crop_bp.route("/register", methods=["POST"])
def register_crop():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    name = data.get("name")

    if not name:
        return jsonify({
            "success": False,
            "message": "Crop name is required"
        }), 400

    crop = Crop(
        name=name
    )

    db.session.add(crop)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Crop added successfully",
        "crop": {
            "id": crop.id,
            "name": crop.name
        }
    }), 201


# --------------------------------------------------
# GET ALL CROPS
# GET /api/crops/all
# --------------------------------------------------
@crop_bp.route("/all", methods=["GET"])
def get_all_crops():

    crops = Crop.query.all()

    crop_list = []

    for crop in crops:
        crop_list.append({
            "id": crop.id,
            "name": crop.name
        })

    return jsonify({
        "success": True,
        "crops": crop_list
    }), 200


# --------------------------------------------------
# GET CROP BY ID
# GET /api/crops/<id>
# --------------------------------------------------
@crop_bp.route("/<int:crop_id>", methods=["GET"])
def get_crop(crop_id):

    crop = Crop.query.get(crop_id)

    if not crop:
        return jsonify({
            "success": False,
            "message": "Crop not found"
        }), 404

    return jsonify({
        "success": True,
        "crop": {
            "id": crop.id,
            "name": crop.name
        }
    }), 200