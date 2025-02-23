from flask_socketio import emit
from app import socketio

import random


@socketio.on("seating_plan")
def handle_request(json_data):
    
    timestamp = json_data.get("timestamp")
    if (timestamp):
        data = [[random.random() for _ in range(5)] for _ in range(8)]
        emit("response", {"timestamp": timestamp, "data": data})
    else:
        emit("response", {"error": 400, "error_message": "No Timestamp provided in request"})
