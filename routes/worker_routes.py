from flask import Blueprint, request, jsonify
from models import db, Worker

worker_bp = Blueprint("worker", __name__)


# --------------------------------------------------
# REGISTER WORKER
# POST /api/workers/register
# --------------------------------------------------
@worker_bp.route("/register", methods=["POST"])
def register_worker():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    name = data.get("name")
    location = data.get("location")
    phone = data.get("phone")
    availability = data.get("availability")

    if not name or not location or not phone:
        return jsonify({
            "success": False,
            "message": "Name, location and phone are required"
        }), 400

    if availability is None:
        availability = True

    worker = Worker(
        name=name,
        village=location,
        phone=phone,
        availability=availability
    )

    db.session.add(worker)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Worker registered successfully",
        "worker": {
            "id": worker.id,
            "name": worker.name,
            "location": worker.village,
            "phone": worker.phone,
            "availability": worker.availability
        }
    }), 201


# --------------------------------------------------
# GET ALL WORKERS
# GET /api/workers/all
# --------------------------------------------------
@worker_bp.route("/all", methods=["GET"])
def get_all_workers():

    workers = Worker.query.all()

    worker_list = []

    for worker in workers:
        worker_list.append({
            "id": worker.id,
            "name": worker.name,
            "location": worker.village,
            "phone": worker.phone,
            "availability": worker.availability
        })

    return jsonify({
        "success": True,
        "workers": worker_list
    }), 200


# --------------------------------------------------
# GET WORKER BY ID
# GET /api/workers/<id>
# --------------------------------------------------
@worker_bp.route("/<int:worker_id>", methods=["GET"])
def get_worker(worker_id):

    worker = Worker.query.get(worker_id)

    if not worker:
        return jsonify({
            "success": False,
            "message": "Worker not found"
        }), 404

    return jsonify({
        "success": True,
        "worker": {
            "id": worker.id,
            "name": worker.name,
            "location": worker.village,
            "phone": worker.phone,
            "availability": worker.availability
        }
    }), 200