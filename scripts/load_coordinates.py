import json
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def load_sensor_metadata(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data["sensors"]


def write_coordinates_to_db(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the table if exists
    cursor.execute("DROP TABLE IF EXISTS coordinates")

    # Create the coordinates table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE coordinates (
            sensor_id TEXT PRIMARY KEY,
            x REAL,
            y REAL,
            zf REAL
        )
    """
    )
    # Insert the coordinate information into the table
    for sensor in data.values():
        sensor_id = sensor["acp_id"]
        sensor_location = sensor["acp_location"]
        x = sensor_location["x"]
        y = sensor_location["y"]
        zf = sensor_location["zf"]
        cursor.execute(
            """
            INSERT OR REPLACE INTO coordinates (sensor_id, x, y, zf)
            VALUES (?, ?, ?, ?)
        """,
            (sensor_id, x, y, zf),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Path to the sensor metadata file
    metadata_file_path = "data/sensor_locations.json"

    # Path to the coordinates database
    db_path = "data/database.db"

    # Load sensor metadata from the file
    sensor_metadata = load_sensor_metadata(metadata_file_path)

    # Write coordinate information into the database
    write_coordinates_to_db(sensor_metadata, db_path)

    print("Coordinates inserted into the database")
