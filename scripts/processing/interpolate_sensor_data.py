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
    locations: List[Tuple[float, float]], timestamp: float
) -> List[Dict]:
    """
    Interpolate sensor data for a given list of locations.

    Args:
    locations: A list of tuples of floats (x, y, z) representing the locations to interpolate sensor data for.
    timestamp: A float representing the timestamp to interpolate sensor data for.

    Returns:
    A list of dictionaries containing the interpolated sensor data for each location.
    """
    # Fetch sensor data records
    results = get_sensor_data(timestamp)

    # Interpolate the sensor data
    sensor_locations = [(result["x"], result["y"]) for result in results]

    interpolated_data = [{} for _ in range(len(locations))]  # Initialize interpolated data
    for feature in ["temperature", "humidity", "co2", "zf"]:
        interpolated_values = griddata(
            sensor_locations,
            [result[feature] for result in results],
            locations,
            method="linear",
        )
        for i, value in enumerate(interpolated_values):
            interpolated_data[i][feature] = value

    return interpolated_data
