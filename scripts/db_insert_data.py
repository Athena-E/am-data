import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tqdm import tqdm

from app.database import get_db
from run import app

# methods for creating records and inserting into database

def insert_sensor_data(data):
    # insert single record of extracted data into database
    sensor_id = data.get("acp_id")
    timestamp = data.get("acp_ts")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    co2 = data.get("co2")

    if all(v is not None for v in (timestamp, temperature, humidity, co2)):
        with app.app_context():

            db = get_db()
            # check for duplicate records
            # cursor = db.cursor()
            # cursor.execute("SELECT * FROM sensor_data WHERE timestamp = ? AND sensor_id = ?", (timestamp,sensor_id))
            # existing = cursor.fetchone()

            # if not existing:
            # Added (OR IGNORE)
            query = '''
            INSERT OR IGNORE INTO sensor_data (sensor_id, timestamp, temperature, humidity, co2)
            VALUES (?, ?, ?, ?, ?)
            '''

            db.execute(query, (sensor_id, timestamp, temperature, humidity, co2))
            db.commit()


def insert_list_sensor_data(data_list):
    # insert list of extracted data into database
    for data in tqdm(data_list, desc="Inserting sensor data", unit="item"):
        insert_sensor_data(data)

