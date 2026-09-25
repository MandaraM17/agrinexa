from flask import Blueprint, request
import requests
import json
import math


weather_bp = Blueprint("weather", __name__)


# ---------------- WEATHER API ----------------

@weather_bp.route("/", methods=["GET"])
def get_weather():

    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return {
            "error": "Latitude and longitude are required"
        }, 400

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": 7,
        "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return {
                "error": "Weather service failed"
            }, 500

        return response.json()

    except requests.RequestException:
        return {
            "error": "Unable to connect to weather service"
        }, 500


# ---------------- DISTANCE CALCULATION ----------------

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = lat2 - lat1
    dlon = math.radians(lon2) - math.radians(lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# ---------------- NEARBY SOCIETIES API ----------------

@weather_bp.route("/societies", methods=["GET"])
def get_societies():

    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return {
            "error": "Latitude and longitude are required"
        }, 400

    try:

        latitude = float(latitude)
        longitude = float(longitude)

        with open("data/societies.json", "r") as file:
            societies = json.load(file)

        nearby = []

        for society in societies:

            distance = calculate_distance(
                latitude,
                longitude,
                society["latitude"],
                society["longitude"]
            )

            if distance <= 20:

                society_data = society.copy()
                society_data["distance_km"] = round(distance, 2)

                nearby.append(society_data)

        nearby.sort(
            key=lambda x: x["distance_km"]
        )

        return {
            "count": len(nearby),
            "societies": nearby
        }

    except ValueError:
        return {
            "error": "Invalid latitude or longitude"
        }, 400

    except FileNotFoundError:
        return {
            "error": "societies.json file not found"
        }, 500

    except Exception as e:
        return {
            "error": str(e)
        }, 500