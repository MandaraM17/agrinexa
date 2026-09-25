from flask import Blueprint, request
from models import db, Worker


worker_bp = Blueprint("worker", __name__)


@worker_bp.route("/", methods=["GET"])
def worker_home():
    return {
        "message": "Worker API is working!"
    }


@worker_bp.route("/register", methods=["POST"])
def register_worker():

    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    village = data.get("village")
    work_type = data.get("work_type")
    experience = data.get("experience")

    if not name or not phone or not village or not work_type:
        return {
            "error": "Name, phone, village and work type are required"
        }, 400

    worker = Worker(
        name=name,
        phone=phone,
        village=village,
        work_type=work_type,
        experience=experience
    )

    db.session.add(worker)
    db.session.commit()

    return {
        "message": "Worker registered successfully!",
        "worker_id": worker.id
    }, 201


@worker_bp.route("/all", methods=["GET"])
def get_all_workers():

    workers = Worker.query.all()

    worker_list = []

    for worker in workers:
        worker_list.append({
            "id": worker.id,
            "name": worker.name,
            "phone": worker.phone,
            "village": worker.village,
            "work_type": worker.work_type,
            "experience": worker.experience
        })

    return {
        "workers": worker_list
    }


@worker_bp.route("/<int:worker_id>", methods=["GET"])
def get_worker(worker_id):

    worker = Worker.query.get(worker_id)

    if not worker:
        return {
            "error": "Worker not found"
        }, 404

    return {
        "id": worker.id,
        "name": worker.name,
        "phone": worker.phone,
        "village": worker.village,
        "work_type": worker.work_type,
        "experience": worker.experience
    }