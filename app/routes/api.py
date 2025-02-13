from flask import Blueprint, jsonify
from scripts.database import get_db

api_bp = Blueprint("api", __name__)

@api_bp.route("/sensors", methods=["GET"])
def get_sensors():
    db = get_db()
    cursor = db.execute("SELECT timestamp, temperature, humidity FROM sensor_data")
    data = cursor.fetchall()
    return jsonify([{"timestamp": row["timestamp"], "temperature": row["temperature"], "humidity": row["humidity"]} for row in data])
