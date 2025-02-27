from ..db_handler import DatabaseHandler, DATABASE
from .visualisations.view_day import plot_sensor_data
from .utils.calculus import differentiate

import pandas as pd
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt

TEST_DATE = '2025-02-07'


def analyse_lecture(seats_occupied):
    print(seats_occupied)
    for seat in seats_occupied.values():

        timestamps = [point[0] for point in seat]
        values1 = [point[1] for point in seat]
        values2 = [point[2] for point in seat]

        # Creating scatter plot
        plt.figure(figsize=(10, 5))
        plt.scatter(timestamps, values1, color='blue', label='Seat Confidence')
        plt.scatter(timestamps, values2, color='red', label='Model Confidence')

        # Formatting plot
        plt.xlabel("Timestamp")
        plt.ylabel("Values")
        plt.title("Scatter Plot of Data")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)

        # Show plot
        plt.show()

def test():

    df = DatabaseHandler.get_all('occupency')

    df = df[(df["timestamp"] > 1738886400) & (df["timestamp"] < 1738972800)]
    df.reset_index(drop=True, inplace=True)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    seats_occupied = defaultdict(list)

    next_lecture_ts = DatabaseHandler.get_next_lecture_ts(df["timestamp"].iloc[0])
    curr_lecture = DatabaseHandler.get_lecture_by_ts(df["timestamp"].iloc[0])
    for i in df.index:

        timestamp = df["timestamp"].iloc[i]

        if timestamp > int(next_lecture_ts):

            if curr_lecture:
                analyse_lecture(seats_occupied)
                seats_occupied = defaultdict(list)
                return

            next_lecture_ts = DatabaseHandler.get_next_lecture_ts(timestamp)
            curr_lecture = DatabaseHandler.get_lecture_by_ts(timestamp)
        


        if curr_lecture:

            cursor.execute("SELECT * FROM seats WHERE occupency_id = ?", (int(df["id"].iloc[i]),))
            result = cursor.fetchall()
            for seat in result:
                seats_occupied[seat[2]].append((timestamp, seat[3], seat[4]))
            

# Filter by average crowd count and sum of model confidence