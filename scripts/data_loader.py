import json 

# methods for parsing and loading data from raw files

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
    }
    return payload_obj

def get_day_data(fname):
    # returns list of JSON extracted data for a preprocessed data file
    filename = f"../data/preprocessed/{fname}"
    day_data = []
    with open(filename, "r") as file:
        for line in file:
            try:
                payload_obj = extract_payload(line)
                day_data.append(payload_obj)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")
    return day_data

