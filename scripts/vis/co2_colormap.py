import numpy as np
import matplotlib.pyplot as plt
from scripts.processing.get_interpolated_data_at_each_seat import (
    get_interpolated_data_at_each_seat,
)


def plot_2d_colormap(timestamp: float, feature: str = "co2", resolution: int = 50):
    """
    Create a 2D color map plot of sensor data across seat locations.

    Args:
        timestamp: float, Unix timestamp to get data for
        feature: str, which feature to plot ('co2', 'temperature', or 'humidity')
        resolution: int, number of points in each dimension for interpolation grid
    """
    seat_data = get_interpolated_data_at_each_seat(timestamp)

    x = np.array([data["x"] for data in seat_data])
    y = np.array([data["y"] for data in seat_data])
    values = np.array([data[feature] for data in seat_data])

    x_min, x_max = x.min() - 10, x.max() + 10
    y_min, y_max = y.min() - 10, y.max() + 10

    # Add corners with the average value of the data to deal with NaNs
    avg_value = np.mean(values)
    x = np.append(x, [x_min, x_min, x_max, x_max])
    y = np.append(y, [y_min, y_max, y_min, y_max])
    values = np.append(values, [avg_value, avg_value, avg_value, avg_value])

    xi = np.linspace(x_min, x_max, resolution)
    yi = np.linspace(y_min, y_max, resolution)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate
    from scipy.interpolate import griddata

    zi = griddata((x, y), values, (xi, yi), method="cubic")

    plt.figure(figsize=(10, 8))

    # Create color map
    mesh = plt.pcolormesh(xi, yi, zi, cmap="viridis", shading="auto")
    # Add seat locations as scatter points
    plt.scatter(x, y, c="red", s=30, alpha=0.5, label="Seat Locations")

    plt.colorbar(mesh, label=f"{feature.capitalize()} Level")

    plt.xlabel("X Coordinate (m)")
    plt.ylabel("Y Coordinate (m)")
    plt.title(f"{feature.capitalize()} Distribution Across Room")

    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend()

    # Make the plot aspect ratio equal
    plt.axis("equal")

    plt.savefig(f"scripts/vis/{feature}_colormap.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # Example usage
    timestamp = 4031447563.0
    plot_2d_colormap(timestamp, feature="co2", resolution=30)
