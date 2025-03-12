import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from scripts.coordinate_mapping.map_coordinates import get_seat_coordinates_in_wgb
from scripts.db.utils import get_db


def plot_occupancy(timestamp: float):
    """
    Plot occupancy levels at a given timestamp.

    Args:
        timestamp: float, Unix timestamp to get data for
    """
    db = get_db()

    # Fetch occupancy data with the closest timestamp for each seat
    occupancy_data = db.execute(
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

    seat_dict = get_seat_coordinates_in_wgb()
    # Extract coordinates and occupancy values
    x = []
    y = []
    crowdcount = []
    for row in occupancy_data:
        seat = row["seat"]
        if seat in seat_dict:
            x.append(seat_dict[seat][0])
            y.append(seat_dict[seat][1])
            crowdcount.append(row["crowdcount"])

    x = np.array(x)
    y = np.array(y)
    crowdcount = np.array(crowdcount)

    # Plot the occupancy levels
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(x, y, c=crowdcount, cmap="viridis", s=100, alpha=0.75)
    plt.colorbar(scatter, label="Occupancy Level")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Occupancy Levels at Timestamp {}".format(timestamp))
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.savefig("scripts/vis/occupancy_levels.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    timestamp = 1738938183.0  # 2pm
    plot_occupancy(timestamp)
