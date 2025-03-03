import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scripts.db.utils import get_db
from scripts.processing.get_interpolated_data_at_each_seat import (
    get_interpolated_data_at_each_seat,
)
from scipy.interpolate import griddata

from datetime import datetime

def plot_2d_colormap_animation(timestamps, feature="co2", resolution=50, interval=1000):
    """
    Create an animated 2D color map plot of sensor data across seat locations over time.

    Args:
        timestamps: list of float, Unix timestamps to get data for
        feature: str, which feature to plot ('co2', 'temperature', or 'humidity')
        resolution: int, number of points in each dimension for interpolation grid
        interval: int, delay between frames in milliseconds
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Normalize the color map across all timestamps
    all_values = []
    for timestamp in timestamps:
        seat_data = get_interpolated_data_at_each_seat(timestamp)
        values = np.array([data[feature] for data in seat_data])
        all_values.extend(values)
    vmin, vmax = min(all_values), max(all_values)

    def update(timestamp):
        print('Processing:', timestamp)
        ax.clear()
        seat_data = get_interpolated_data_at_each_seat(timestamp)

        x = np.array([data["x"] for data in seat_data])
        y = np.array([data["y"] for data in seat_data])
        values = np.array([data[feature] for data in seat_data])

        x_min, x_max = x.min() - 10, x.max() + 10
        y_min, y_max = y.min() - 10, y.max() + 10

        avg_value = np.mean(values)
        x = np.append(x, [x_min, x_min, x_max, x_max])
        y = np.append(y, [y_min, y_max, y_min, y_max])
        values = np.append(values, [avg_value, avg_value, avg_value, avg_value])

        xi = np.linspace(x_min, x_max, resolution)
        yi = np.linspace(y_min, y_max, resolution)
        xi, yi = np.meshgrid(xi, yi)

        zi = griddata((x, y), values, (xi, yi), method="cubic")

        mesh = ax.pcolormesh(xi, yi, zi, cmap="viridis", shading="auto", vmin=vmin, vmax=vmax)
        ax.scatter(x, y, c="red", s=30, alpha=0.5, label="Seat Locations")

        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")

        timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        ax.set_title(f"{feature.capitalize()} Distribution Across Room at {timestamp}")

        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend()
        ax.axis("equal")

        # Add color bar
        if not hasattr(update, "colorbar"):
            update.colorbar = fig.colorbar(mesh, ax=ax, orientation="vertical")
        else:
            update.colorbar.update_normal(mesh)

        return mesh,

    ani = FuncAnimation(fig, update, frames=timestamps, interval=interval, blit=False)

    ani.save(f"scripts/vis/{feature}_colormap_animation.gif", writer="imagemagick", dpi=100)
    # plt.show()


if __name__ == "__main__":
    # Example usage
    db = get_db()
    min_timestamp, max_timestamp = db.execute(
        "SELECT MIN(timestamp), MAX(timestamp) FROM clean_sensor_data"
    ).fetchone()
    timestamps = np.linspace(int(min_timestamp), int(max_timestamp), 24 * 2).tolist()
    plot_2d_colormap_animation(timestamps, feature="humidity", resolution=30, interval=100)
