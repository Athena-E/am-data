import numpy as np
import matplotlib.pyplot as plt

from scripts.db.utils import get_db


def plot_co2_data():
    db = get_db()
    motion_data = db.execute(
        """
            SELECT timestamp, motion, sensor_id
            FROM clean_sensor_data 
            WHERE co2 IS NOT NULL
        """
    ).fetchall()
    timestamps, motions, sensors = zip(*motion_data)
    timestamps, motions, sensors = (
        np.array(timestamps),
        np.array(motions),
        np.array(sensors),
    )

    # Convert timestamps to hours
    timestamps = (
        (timestamps - timestamps.min()) / (timestamps.max() - timestamps.min()) * 24
    )

    unique_sensors = np.unique(sensors)

    plt.figure(figsize=(10, 6))

    for sensor in unique_sensors:
        sensor_mask = sensors == sensor
        plt.plot(
            timestamps[sensor_mask], motions[sensor_mask], label=f"Sensor {sensor}"
        )

    plt.xlabel("Hour")
    plt.ylabel("Motion")
    plt.title("Motion Data by Sensor")
    plt.ylim(0, 3)
    plt.xlim(0, 24)
    plt.savefig("./scripts/vis/motion.png")
    plt.show()


if __name__ == "__main__":
    plot_co2_data()
