from flask import Blueprint, request
from models import db, Crop

crop_bp = Blueprint("crop", __name__)


@crop_bp.route("/add", methods=["POST"])
def add_crop():
    data = request.get_json()

    name = data.get("name")
    crop_type = data.get("crop_type")
    area = data.get("area")
    planting_date = data.get("planting_date")
    farmer_id = data.get("farmer_id")

    if not name or not crop_type or not area or not planting_date or not farmer_id:
        return {
            "error": "All crop details are required"
        }, 400

    crop = Crop(
        name=name,
        crop_type=crop_type,
        area=area,
        planting_date=planting_date,
        farmer_id=farmer_id
    )

    db.session.add(crop)
    db.session.commit()

    return {
        "message": "Crop added successfully!",
        "crop_id": crop.id
    }, 201


@crop_bp.route("/all", methods=["GET"])
def get_all_crops():
    crops = Crop.query.all()

    crop_list = []

    for crop in crops:
        crop_list.append({
            "id": crop.id,
            "name": crop.name,
            "crop_type": crop.crop_type,
            "area": crop.area,
            "planting_date": crop.planting_date,
            "farmer_id": crop.farmer_id
        })

    return {
        "crops": crop_list
    }