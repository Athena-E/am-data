from flask import Blueprint, jsonify, request, make_response
from scripts.db.utils import get_db

api_bp = Blueprint("api", __name__)

@api_bp.route("/sensors", methods=["GET"])
def get_sensors():
    db = get_db()
    cursor = db.execute("SELECT timestamp, temperature, humidity FROM sensor_data")
    data = cursor.fetchall()
    return jsonify([{"timestamp": row["timestamp"], "temperature": row["temperature"], "humidity": row["humidity"]} for row in data])


@api_bp.route("/sensor_data", methods=["GET"])
def get_sensor_data_at_ts():
    timestamp = request.args.get("timestamp")  
    # sensor_id = request.args.get("sensor_id")
    
    if not timestamp:
        return make_response(jsonify({"error": "Missing timestamp in request"}), 400)
    # if not sensor_id:
    #     return make_response(jsonify({"error": "Missing sensor_id in request"}), 400)

    db = get_db()
    cursor = db.execute(
        "SELECT timestamp, temperature, humidity FROM clean_sensor_data WHERE timestamp = ?",
        (timestamp,)
    )
    data = cursor.fetchall()  
    
    if data:
        return jsonify([{"timestamp": row["timestamp"], "co2": row["co2"], "temperature": row["temperature"], "humidity": row["humidity"]} for row in data])
    else:
        return make_response(jsonify({"error": "No data found for the given timestamp"}), 404)


@api_bp.route("/coordinates", methods=["GET"])
def get_sensor_coordinates():
    db = get_db()
    cursor = db.execute("SELECT sensor_id, x, y, zf FROM coordinates")
    data = cursor.fetchall()
    return jsonify([{"timestamp": row["timestamp"], "temperature": row["temperature"], "humidity": row["humidity"]} for row in data])


@api_bp.route("/timetable", methods=["GET"])
def get_full_timetable():
    # general method for getting all timetable data
    db = get_db()
    cursor = db.execute("SELECT uid, lecture_name, start, end FROM timetable")
    data = cursor.fetchall()
    return jsonify([{"uid": row["uid"], "lecture_name": row["lecture_name"], "start": row["start"], "end": row["end"]} for row in data])


@api_bp.route("/timetable", methods=["GET"])
def get_lecture_by_ts():
    # get lecture name from current timestamp
    timestamp = request.args.get("timestamp")  

    if not timestamp:
        return make_response(jsonify({"error": "Missing timestamp in request"}), 400)

    db = get_db()
    cursor = db.execute(
        "SELECT uid, lecture_name, start, end FROM timetable WHERE ? BETWEEN start AND end",
        (timestamp,)
    )
    data = cursor.fetchone()
    
    if data:
        return jsonify({"lecture_name": data["lecture_name"], "uid": data["uid"]})
    else:
        return make_response(jsonify({"error": "No data found for the given timestamp"}), 404)
