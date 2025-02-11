import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tqdm import tqdm
from app.database import get_db
from run import app

def insert_list_sensor_data(data_list):
    """ Insert a list of extracted sensor data into the database efficiently. """
    with app.app_context():
        db = get_db()
        query = '''
        INSERT OR IGNORE INTO sensor_data (sensor_id, timestamp, temperature, humidity, co2)
        VALUES (?, ?, ?, ?, ?)
        '''
        
        # Convert list of dictionaries to a list of tuples
        records = [
            (data["acp_id"], data["acp_ts"], data["temperature"], data["humidity"], data["co2"])
            for data in data_list
            if all(k in data for k in ("acp_id", "acp_ts", "temperature", "humidity", "co2"))
        ]

        if records:
            db.executemany(query, records)
            db.commit()
