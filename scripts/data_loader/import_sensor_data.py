import os
import json

from scripts.db.insert_data import insert_list_sensor_data


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



# calls methods to load and insert sensor data

def import_sensor_data():
    # Add all data to the database from preprocessed folder
    
    PREPROCESSED_DIR = './data/preprocessed'

    # get all preprocessed day data files
    data_files = [f for f in os.listdir(PREPROCESSED_DIR) if os.path.isfile(os.path.join(PREPROCESSED_DIR, f))]

    all_extracted = []
    for f in data_files:
        all_extracted += get_day_data(f)
    
    insert_list_sensor_data(all_extracted)
