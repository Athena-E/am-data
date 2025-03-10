CREATE TABLE IF NOT EXISTS clean_sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT NOT NULL,
    timestamp REAL NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    co2 REAL NOT NULL,
    motion REAL NOT NULL,
    UNIQUE(sensor_id, timestamp)
);
