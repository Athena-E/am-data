import numpy as np
import matplotlib.pyplot as plt

from scripts.db.utils import get_db


def plot_co2_data():
    # Connect to the SQLite database
    db = get_db()

    co2_data = db.execute(
        """
            SELECT timestamp, MIN(co2) as min, MAX(co2) as max, AVG(co2) as avg
            FROM clean_sensor_data 
            WHERE co2 IS NOT NULL
            GROUP BY ROUND(timestamp / 300)
        """
    ).fetchall()
    time, min_co2_levels, max_co2_levels, avg_co2_levels = zip(*co2_data)
    time, min_co2_levels, max_co2_levels, avg_co2_levels = (
        np.array(time),
        np.array(min_co2_levels),
        np.array(max_co2_levels),
        np.array(avg_co2_levels),
    )

    # Plot the graph
    plt.figure(figsize=(8, 4))
    plt.plot(time, avg_co2_levels, color="blue", label="CO2 Levels")
    plt.fill_between(
        time, min_co2_levels, max_co2_levels, color="blue", alpha=0.2
    )  # Shaded region

    # Labels and title
    plt.xlabel("Time (hours)")
    plt.ylabel("[CO2] (ppm)")
    plt.title("CO2 Concentration Over Time")

    # Label x-axis from 0 to 24 hours
    plt.xticks(np.linspace(min(time), max(time), 24), [str(i) for i in range(24)])

    # Show grid and legend
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.savefig("scripts/vis/co2_levels.png")
    plt.show()


if __name__ == "__main__":
    plot_co2_data()
