import os
import json

from scripts.db.utils import get_db


def extract_payload(data):
    # returns JSON of id, timestamp, payload from full JSON sensor data
    parsed_data = json.loads(data)
    sensor_id = parsed_data.get("acp_id").split("elsys-co2-")[-1]
    payload_obj = {
        "acp_id": sensor_id,
        "acp_ts": parsed_data.get("acp_ts"),
        "temperature": parsed_data.get("payload_cooked", {}).get("temperature"),
        "humidity": parsed_data.get("payload_cooked", {}).get("humidity"),
        "co2": parsed_data.get("payload_cooked", {}).get("co2"),
        "motion": parsed_data.get("payload_cooked", {}).get("motion"),
    }
    return payload_obj


def get_day_data(fname):
    # returns list of JSON extracted data for a preprocessed data file
    filename = f"./data/preprocessed/{fname}"
    day_data = []
    with open(filename, "r") as file:
        for line in file:
            try:
                payload_obj = extract_payload(line)
                day_data.append(payload_obj)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")
    return day_data


def insert_list_sensor_data(data_list):
    db = get_db()
    query = """
    INSERT OR IGNORE INTO sensor_data (sensor_id, timestamp, temperature, humidity, co2, motion)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    records = [
        (
            data["acp_id"],
            data["acp_ts"],
            data["temperature"],
            data["humidity"],
            data["co2"],
            data["motion"],
        )
        for data in data_list
        if all(
            k in data
            for k in ("acp_id", "acp_ts", "temperature", "humidity", "co2", "motion")
        )
    ]

    if records:
        db.executemany(query, records)
        db.commit()


# Add all sensor data to the database from preprocessed folder
def import_sensor_data():
    PREPROCESSED_DIR = "./data/preprocessed"

    # get all preprocessed day data files
    data_files = [
        f
        for f in os.listdir(PREPROCESSED_DIR)
        if os.path.isfile(os.path.join(PREPROCESSED_DIR, f))
    ]

    all_extracted = []
    for f in data_files:
        all_extracted += get_day_data(f)

    insert_list_sensor_data(all_extracted)
