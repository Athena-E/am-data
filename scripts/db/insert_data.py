from scripts.db.utils import get_db

DATABASE = "./data/database.db"

# insert sensor data into database

def insert_list_sensor_data(data_list):
    db = get_db()
    query = '''
    INSERT OR IGNORE INTO sensor_data (sensor_id, timestamp, temperature, humidity, co2, motion)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    
    records = [
        (data["acp_id"], data["acp_ts"], data["temperature"], data["humidity"], data["co2"], data['motion'])
        for data in data_list
        if all(k in data for k in ("acp_id", "acp_ts", "temperature", "humidity", "co2", "motion"))
    ]

    if records:
        db.executemany(query, records)
        db.commit()
