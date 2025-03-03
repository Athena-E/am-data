import numpy as np
import json
from scipy.interpolate import griddata
from scripts.processing.get_interpolated_data_at_each_seat import (
    get_interpolated_data_at_each_seat,
)
from scripts.db.utils import get_db


def get_co2_and_danger_uniform_map(timestamp: float, n: int = 50):
    """
    Generate an n x n grid of CO2 values interpolated across seat locations,
    with normalized x and y coordinates, and return as JSON.

    Args:
        timestamp: float, Unix timestamp to get data for
        n: int, number of grid points in each dimension

    Returns:
        json_data: JSON object with CO2 values, danger values, and normalized (x, y) coordinates
    """
    db = get_db()

    # Get interpolated data at each seat
    seat_data = get_interpolated_data_at_each_seat(timestamp)

    # Fetch occupency data with the closest timestamp for each seat
    occupency_data = db.execute(
        """
        WITH ranked_occupency AS (
            SELECT seat, crowdcount, timestamp,
                   ROW_NUMBER() OVER (PARTITION BY seat ORDER BY ABS(timestamp - ?) ASC) AS rank
            FROM occupency
            JOIN seats ON occupency.id = seats.occupency_id
        )
        SELECT seat, crowdcount
        FROM ranked_occupency
        WHERE rank = 1
        """,
        (timestamp,),
    ).fetchall()
    occupency_dict = {row["seat"]: row["crowdcount"] for row in occupency_data}

    # Extract coordinates and values
    x = np.array([data["x"] for data in seat_data])
    y = np.array([data["y"] for data in seat_data])
    co2_values = np.array([data["co2"] for data in seat_data])
    crowdcount_values = np.array(
        [occupency_dict.get(data["seat_id"], 0) for data in seat_data]
    )

    # Smooth crowdcount values using a simple moving average
    window_size = 9
    crowdcount_values = np.convolve(crowdcount_values, np.ones(window_size)/window_size, mode='same')
    danger_values = (co2_values-300) * (crowdcount_values + 1)

    # Define grid boundaries
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Normalize x and y coordinates
    if x_max > x_min:
        x_norm = (x - x_min) / (x_max - x_min)
    else:
        x_norm = np.zeros_like(x)

    if y_max > y_min:
        y_norm = (y - y_min) / (y_max - y_min)
    else:
        y_norm = np.zeros_like(y)

    # Generate normalized grid
    xi = np.linspace(0, 1, n)
    yi = np.linspace(0, 1, n)
    xi, yi = np.meshgrid(xi, yi)

    co2_zi = griddata((x_norm, y_norm), co2_values, (xi, yi), method="linear")
    danger_zi = griddata((x_norm, y_norm), danger_values, (xi, yi), method="linear")

    # Fill NaNs with nearest neighbor interpolation
    if np.isnan(co2_zi).any():
        co2_zi = griddata((x_norm, y_norm), co2_values, (xi, yi), method="nearest")
    if np.isnan(danger_zi).any():
        danger_zi = griddata(
            (x_norm, y_norm), danger_values, (xi, yi), method="nearest"
        )

    co2_and_danger_map = []
    for i in range(n):
        for j in range(n):
            co2_and_danger_map.append(
                {
                    "x": float(xi[i, j]),
                    "y": float(yi[i, j]),
                    "co2": float(co2_zi[i, j]),
                    "danger": float(danger_zi[i, j]),
                }
            )

    return co2_and_danger_map


def save_to_json(map, filename="./scripts/processing/co2_and_danger_uniform_map.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(map, f, indent=4)


if __name__ == "__main__":
    timestamp = 1738938183.35689  # Replace with your desired timestamp
    co2_and_danger_uniform_map = get_co2_and_danger_uniform_map(timestamp)
    save_to_json(co2_and_danger_uniform_map)
