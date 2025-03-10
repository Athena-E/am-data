import numpy as np
import json
from scipy.interpolate import griddata
from scripts.processing.get_interpolated_data_at_each_seat import (
    get_interpolated_data_at_each_seat,
)
from scripts.db.utils import get_db
from datetime import datetime, timedelta
from multiprocessing import Pool


def get_co2_and_danger_uniform_map(
    seat_data, occupancy_dict, timestamp: float, n: int = 50
):
    """
    Generate an n x n grid of CO2 values interpolated across seat locations,
    with normalized x and y coordinates, and return as JSON.

    Args:
        timestamp: float, Unix timestamp to get data for
        n: int, number of grid points in each dimension

    Returns:
        json_data: JSON object with CO2 values, danger values, and normalized (x, y) coordinates
    """
    # Extract coordinates and values
    x = np.array([data["x"] for data in seat_data])
    y = np.array([data["y"] for data in seat_data])
    co2_values = np.array([data["co2"] for data in seat_data])
    crowdcount_values = np.array(
        [occupancy_dict.get(data["seat_id"], 0) for data in seat_data]
    )

    # Smooth crowdcount values using a simple moving average
    window_size = 9
    crowdcount_values = np.convolve(
        crowdcount_values, np.ones(window_size) / window_size, mode="same"
    )
    danger_values = (co2_values - 300) * (crowdcount_values + 1)

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

    co2_zi = griddata((x_norm, y_norm), co2_values, (xi, yi), method="cubic")
    danger_zi = griddata((x_norm, y_norm), danger_values, (xi, yi), method="cubic")

    # Fill NaNs with nearest neighbor interpolation
    if np.isnan(co2_zi).any():
        co2_zi = griddata((x_norm, y_norm), co2_values, (xi, yi), method="nearest")
    if np.isnan(danger_zi).any():
        danger_zi = griddata(
            (x_norm, y_norm), danger_values, (xi, yi), method="nearest"
        )

    co2_and_danger_map = [
        {
            "x": round(float(xi[i, j]), 5),
            "y": round(float(yi[i, j]), 5),
            "co2": round(float(co2_zi[i, j]), 5),
            "danger": round(float(danger_zi[i, j]), 5),
        }
        for i in range(n)
        for j in range(n)
    ]

    print("Processed:", datetime.fromtimestamp(timestamp))
    return {"timestamp": timestamp, "data": co2_and_danger_map}


def save_to_json(map, filename="./scripts/processing/co2_and_danger_uniform_map.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(map, f, separators=(",", ":"))


def process_timestamp(args):
    seat_data, occupancy_dict, timestamp, n = args
    return get_co2_and_danger_uniform_map(seat_data, occupancy_dict, timestamp, n)


if __name__ == "__main__":
    db = get_db()

    # Fetch all seat data
    seat_data = get_interpolated_data_at_each_seat(
        0
    )  # Use any timestamp to get seat data structure

    # Fetch all occupancy data
    occupancy_data = db.execute(
        "SELECT seat, crowdcount, timestamp FROM occupency JOIN seats ON occupency.id = seats.occupency_id"
    ).fetchall()
    occupancy_dict = {}
    for row in occupancy_data:
        if row["seat"] not in occupancy_dict:
            occupancy_dict[row["seat"]] = {}
        rounded_timestamp = int(round(row["timestamp"] / 60) * 60)
        occupancy_dict[row["seat"]][row["timestamp"]] = row["crowdcount"]

    # start = datetime(2025, 2, 7, 0, 0)
    # end = datetime(2025, 2, 7, 23, 59)
    # timestamps = [
    #     (start + timedelta(minutes=i)).timestamp()
    #     for i in range(24 * 60)
    # ]

    timestamps = np.array(range(1738886400, 1738972800, 60), dtype=float)

    # Prepare arguments for parallel processing
    args = [
        (
            seat_data,
            {seat: occupancy_dict[seat].get(ts, 0) for seat in occupancy_dict},
            ts,
            50,
        )
        for ts in timestamps
    ]

    # Use multiprocessing to speed up processing
    with Pool() as pool:
        results = pool.map(process_timestamp, args)

    save_to_json(results)
    print("Processed all timestamps.")
