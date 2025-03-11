import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib import image as mpimg

from scripts.db.utils import get_db
from scripts.coordinate_mapping.map_coordinates import wgb_to_seat_coords


def get_lecture_co2_data():
    db = get_db()

    # testing with Logic and Proof, uid = 1204449
    uid = "1204449"
    co2_data = db.execute(
        """
            SELECT c.* FROM clean_sensor_data c
            JOIN timetable t ON c.timestamp BETWEEN t.start AND t.end
            WHERE t.uid = ?
        """,
        (uid,),
    ).fetchall()

    data = [
        {
            "sensor_id": row["sensor_id"],
            "timestamp": row["timestamp"],
            "co2": row["co2"],
        }
        for row in co2_data
    ]
    return data


def get_xy_sensor_coordinates():
    db = get_db()

    coordinates = db.execute(
        """
            SELECT sensor_id, x, y FROM coordinates
        """
    ).fetchall()

    data = [
        {"sensor_id": row["sensor_id"], "x": row["x"], "y": row["y"]}
        for row in coordinates
    ]
    return data


def get_co2_per_sensor():
    data = get_lecture_co2_data()

    sensor_to_co2 = {}
    for entry in data:
        sensor_id = entry["sensor_id"]
        co2 = entry["co2"]
        if sensor_id not in sensor_to_co2:
            sensor_to_co2[sensor_id] = {"timestamps": [], "co2s": []}
        sensor_to_co2[sensor_id]["timestamps"].append(entry["timestamp"])
        sensor_to_co2[sensor_id]["co2s"].append(co2)

    return sensor_to_co2


def plot_lecture_co2_per_sensor():
    sensor_to_co2 = get_co2_per_sensor()

    plt.figure(figsize=(10, 5))

    for sensor_id, values in sensor_to_co2.items():
        timestamps = [ts for ts in values["timestamps"]]
        co2s = values["co2s"]
        plt.plot(timestamps, co2s, label=f"Sensor {sensor_id}")

    plt.title("CO2 Concentration Over Time by Sensor")
    plt.xlabel("Time")
    plt.ylabel("CO2 Concentration (ppm)")
    plt.xticks(rotation=45)
    plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()


def plot_avg_lecture_co2_per_sensor():
    sensor_to_co2 = get_co2_per_sensor()
    sensor_coords = get_xy_sensor_coordinates()

    # Calculate the average CO2 per sensor
    avg_co2_per_sensor = {}
    for sensor_id, values in sensor_to_co2.items():
        avg_co2_per_sensor[sensor_id] = np.mean(values["co2s"])
    print(avg_co2_per_sensor)

    img = mpimg.imread("imgs/LT1_seating_uncompressed.png")
    co2_values = avg_co2_per_sensor.values()
    norm = Normalize(vmin=min(co2_values), vmax=max(co2_values))
    cmap = cm.viridis

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.imshow(img)

    # Extract sensor locations and CO2 values
    sensor_xy = [
        wgb_to_seat_coords(sensor["x"], sensor["y"]) for sensor in sensor_coords
    ]
    sensor_x = [sensor[0] for sensor in sensor_xy]
    sensor_y = [sensor[1] for sensor in sensor_xy]
    sensor_ids = [sensor["sensor_id"] for sensor in sensor_coords]
    sensor_co2 = [avg_co2_per_sensor.get(id[10:], 0) for id in sensor_ids]

    scatter = ax.scatter(
        sensor_x,
        sensor_y,
        c=sensor_co2,
        cmap=cmap,
        norm=norm,
        s=100,
        edgecolors="black",
        label="Sensors",
    )

    cbar = plt.colorbar(scatter, ax=ax, orientation="vertical")
    cbar.set_label("CO2 Concentration")

    ax.set_title("CO2 Concentration Map, Logic and Proof, 07/02/25")
    ax.set_xlabel("X Coordinates")
    ax.set_ylabel("Y Coordinates")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_lecture_co2_per_sensor()
    plot_avg_lecture_co2_per_sensor()
