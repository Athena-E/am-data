import numpy as np
import json
from scipy.interpolate import griddata
from scripts.processing.get_interpolated_data_at_each_seat import (
    get_interpolated_data_at_each_seat,
)

def get_co2_uniform_map(timestamp: float, n: int = 50):
    """
    Generate an n x n grid of CO2 values interpolated across seat locations,
    with normalized x and y coordinates, and return as JSON.

    Args:
        timestamp: float, Unix timestamp to get data for
        n: int, number of grid points in each dimension

    Returns:
        json_data: JSON object with CO2 values and normalized (x, y) coordinates
    """
    # Get interpolated data at each seat
    seat_data = get_interpolated_data_at_each_seat(timestamp)

    # Extract coordinates and values
    x = np.array([data["x"] for data in seat_data])
    y = np.array([data["y"] for data in seat_data])
    values = np.array([data["co2"] for data in seat_data])

    # Define grid boundaries
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Normalize x and y coordinates
    if x_max > x_min: x_norm = (x - x_min) / (x_max - x_min)
    else: x_norm = np.zeros_like(x)

    if y_max > y_min: y_norm = (y - y_min) / (y_max - y_min)
    else: y_norm = np.zeros_like(y)

    # Generate normalised grid
    xi = np.linspace(0, 1, n)
    yi = np.linspace(0, 1, n)
    xi, yi = np.meshgrid(xi, yi)

    zi = griddata((x_norm, y_norm), values, (xi, yi), method="linear")

    # Fill NaNs with nearest neighbor interpolation
    if np.isnan(zi).any():
        zi = griddata((x_norm, y_norm), values, (xi, yi), method="nearest")

    co2_map = []
    for i in range(n):
        for j in range(n):
            co2_map.append({"x": float(xi[i, j]), "y": float(yi[i, j]), "co2": float(zi[i, j])})

    return co2_map

def save_to_json(map, filename="./scripts/processing/co2_uniform_map.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(map, f, indent=4)

if __name__ == "__main__":
    co2_uniform_map = get_co2_uniform_map(1738938183.35689)
    save_to_json(co2_uniform_map)
