from flask import Blueprint
from models import Farmer, Crop


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/<int:farmer_id>", methods=["GET"])
def farmer_dashboard(farmer_id):

    farmer = Farmer.query.get(farmer_id)

    if not farmer:
        return {
            "error": "Farmer not found"
        }, 404

    crops = Crop.query.filter_by(farmer_id=farmer_id).all()

    crop_list = []
    total_area = 0

    for crop in crops:

        crop_list.append({
            "id": crop.id,
            "name": crop.name,
            "crop_type": crop.crop_type,
            "area": crop.area,
            "planting_date": crop.planting_date
        })

        total_area += crop.area

    return {
        "farmer": {
            "id": farmer.id,
            "name": farmer.name,
            "phone": farmer.phone,
            "village": farmer.village
        },
        "summary": {
            "total_crops": len(crops),
            "total_area": total_area
        },
        "crops": crop_list
    }