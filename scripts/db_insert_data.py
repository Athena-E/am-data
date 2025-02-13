from scripts.database import get_db
from run import app

def insert_list_sensor_data(data_list):
    # insert list of sensor data as records into database
    with app.app_context():
        db = get_db()
        query = '''
        INSERT OR IGNORE INTO sensor_data (sensor_id, timestamp, temperature, humidity, co2)
        VALUES (?, ?, ?, ?, ?)
        '''
        
        records = [
            (data["acp_id"], data["acp_ts"], data["temperature"], data["humidity"], data["co2"])
            for data in data_list
            if all(k in data for k in ("acp_id", "acp_ts", "temperature", "humidity", "co2"))
        ]

        if records:
            db.executemany(query, records)
            db.commit()
