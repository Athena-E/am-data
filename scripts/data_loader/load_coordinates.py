import json


def load_sensor_metadata(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data["sensors"]

