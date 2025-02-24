
from scripts.db.utils import get_db
from scripts.data_loader.load_coordinates import load_sensor_metadata


def import_coordinates():
    db = get_db()
    data = load_sensor_metadata('./data/sensor_locations.json')

    # Drop the table if exists
    db.execute("DROP TABLE IF EXISTS coordinates")
    db.commit()

    # Create the coordinates table if it doesn't exist
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
    # Insert the coordinate information into the table
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