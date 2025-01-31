import json 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def get_payload_object(data):
    # extracts id, timestamp, payload from JSON sensor data
    parsed_data = json.loads(data)
    payload_obj = {
        "acp_id": parsed_data.get("acp_id"),
        "acp_ts": parsed_data.get("acp_ts"),
        "payload_cooked": parsed_data.get("payload_cooked")
    }
    return payload_obj

