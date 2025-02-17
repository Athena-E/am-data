import sqlite3
from typing import Tuple, List, Dict
from scripts.db.utils import get_db
from scipy.interpolate import griddata


def get_sensor_data(timestamp: float) -> List[Dict]:
    """
    Fetch sensor data records with the closest timestamp for each sensor.

    Args:
    timestamp: A float representing the timestamp to fetch sensor data for.

    Returns:
    A list of dictionaries containing the sensor data records.
    """
    db = get_db()

    query = """
    WITH ranked_data AS (
        SELECT 
            sd.sensor_id, 
            sd.temperature, 
            sd.humidity, 
            sd.co2, 
            c.x,
            c.y,
            c.zf,
            sd.timestamp,
            ROW_NUMBER() OVER (PARTITION BY sd.sensor_id ORDER BY ABS(sd.timestamp - ?) ASC) AS rank
        FROM sensor_data sd
        JOIN coordinates c ON sd.sensor_id = c.sensor_id
    )
    SELECT sensor_id, temperature, humidity, co2, x, y, zf, timestamp
    FROM ranked_data
    WHERE rank = 1;
    """

    cursor = db.execute(query, (timestamp,))
    results = cursor.fetchall()
    results = [dict(result) for result in results]
    return results


def interpolate_sensor_data(
    location: Tuple[float, float, float], timestamp: float
) -> dict:
    """
    Interpolate sensor data for a given location.

    Args:
    location: A tuple of floats (x, y, z) representing the location to interpolate sensor data for.
    timestamp: A float representing the timestamp to interpolate sensor data for.

    Returns:
    A dictionary containing the interpolated sensor data.
    """
    # Fetch sensor data records
    results = get_sensor_data(timestamp)

    # Interpolate the sensor data
    locations = [(result["x"], result["y"], result["zf"]) for result in results]

    sensor_data = {
        feature: griddata(
            locations,
            [result[feature] for result in results],
            [location],
            method="linear",
        )[0]
        for feature in ["temperature", "humidity", "co2"]
    }

    return sensor_data
