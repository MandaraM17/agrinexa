from flask import Flask
from models import db
from routes.farmer_routes import farmer_bp
from routes.crop_routes import crop_bp
from routes.buyer_routes import buyer_bp
from routes.worker_routes import worker_bp
from routes.dashboard_routes import dashboard_bp
from routes.voice_routes import voice_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agrinexa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(farmer_bp, url_prefix="/api/farmer")
app.register_blueprint(crop_bp, url_prefix="/api/crop")
app.register_blueprint(buyer_bp, url_prefix="/api/buyer")
app.register_blueprint(worker_bp, url_prefix="/api/worker")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
app.register_blueprint(voice_bp,url_prefix="/api/voice")



@app.route("/")
def home():
    return {
        "message": "Agrinexa Backend is Running!"
    }


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)