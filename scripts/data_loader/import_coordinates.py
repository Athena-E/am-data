from scripts.db.utils import get_db
import json


def load_sensor_metadata(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data["sensors"]


# Import sensor location data from sensor metadata
def import_coordinates():
    db = get_db()
    data = load_sensor_metadata("./data/sensor_locations.json")

    db.execute("DROP TABLE IF EXISTS coordinates")
    db.commit()

    db.execute(
        """
        CREATE TABLE coordinates (
            sensor_id TEXT PRIMARY KEY,
            x REAL,
            y REAL,
            zf REAL
        )
        """
    )
    db.commit()

    for sensor in data.values():
        sensor_id = sensor["acp_id"].split("elsys-co2-")[-1]
        sensor_location = sensor["acp_location"]
        x = sensor_location["x"]
        y = sensor_location["y"]
        zf = sensor_location["zf"]
        db.execute(
            """
            INSERT OR REPLACE INTO coordinates (sensor_id, x, y, zf)
            VALUES (?, ?, ?, ?)
        """,
            (sensor_id, x, y, zf),
        )
        db.commit()
