from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    village = db.Column(db.String(100), nullable=False)


class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, nullable=False)
    planting_date = db.Column(db.String(20), nullable=False)
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey("farmer.id"),
        nullable=False
    )


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    village = db.Column(db.String(100), nullable=False)
    work_type = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50))