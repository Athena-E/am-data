from ..db_handler import DatabaseHandler, DATABASE
from .visualisations.view_day import plot_sensor_data
from .utils.calculus import differentiate

import pandas as pd
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

TEST_DATE = '2025-02-07'

def edit_id(id):
    editid = list(id)
    if editid[0] == "R":
        editid[2] = str(6 - int(editid[2]))
    
    second = editid.pop(1)
    editid.append(second)
    
    return "".join(editid)


def analyse_lecture(cursor, crowdcount, seats_occupied):

    seat_scores = []
    for id, data in seats_occupied.items():
        product = (sc*mc for _, _, sc, mc in data)
        sum_of_product = sum(filter(lambda x: x > 0, product))
        seat_scores.append((id, data, sum_of_product))

    seat_scores.sort(key=lambda x: x[2], reverse=True)
    probable_seats = seat_scores[:crowdcount]

    for id, data, _ in probable_seats:

        # timestamps = [point[0] for point in data]
        # seat_confidence = [point[1] for point in data]
        # model_confidence = [point[2] for point in data]
        product = [sc*mc for _, _, sc, mc in data]

        LQ = np.percentile(product, 15)
        UQ = np.percentile(product, 75)

        for ts, occupency_id, sc, mc in data:

            product = sc * mc
            engagement = "NEUTRAL"
            if product > UQ:
                engagement = "HIGH"
            elif product < LQ:
                engagement = "LOW"
            
            seat = edit_id(id)
        
            cursor.execute("INSERT OR REPLACE INTO clean_seats (occupency_id, seat, engagement) VALUES (?, ?, ?)", (occupency_id, seat, engagement))
        
        # product = pd.Series(product)
        # product = product.ewm(alpha=0.3, adjust=False)
        # print(product)
        # print(product.mean())
        # product = product.mean()

        # Creating scatter plot
        # plt.figure(figsize=(10, 5))
        # plt.plot(timestamps, seat_confidence, color='blue', label='Seat Confidence')
        # plt.plot(timestamps, model_confidence, color='red', label='Model Confidence')
        # plt.plot(timestamps, product, color='green', label='Product')

        # plt.axhline(LQ, color='g', linestyle='--', label=f"Q1 (25th percentile): {LQ:.2f}")
        # plt.axhline(UQ, color='g', linestyle='--', label=f"Q3 (75th percentile): {UQ:.2f}")

        # # Formatting plot
        # plt.xlabel("Timestamp")
        # plt.ylabel("Values")
        # plt.title("Scatter Plot of Data")
        # plt.legend()
        # plt.xticks(rotation=45)
        # plt.grid(True)

        # # Show plot
        # plt.show()

def test():

    df = DatabaseHandler.get_all('occupency')

    df = df[(df["timestamp"] > 1738886400) & (df["timestamp"] < 1738972800)]
    df.reset_index(drop=True, inplace=True)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    seats_occupied = defaultdict(list)
    crowdcounts = []

    next_lecture_ts = DatabaseHandler.get_next_lecture_ts(df["timestamp"].iloc[0])
    curr_lecture = DatabaseHandler.get_lecture_by_ts(df["timestamp"].iloc[0])
    for i in df.index:

        timestamp = df["timestamp"].iloc[i]

        if timestamp > int(next_lecture_ts):

            if curr_lecture:
                q1, q3 = int(len(crowdcounts) * 0.25), int(len(crowdcounts) * 0.75)
                crowdcount = int(sum(crowdcounts[q1:q3]) / (q3 - q1))
                print("Analyzing lecture", curr_lecture[1], "with crowd count", crowdcount)
                analyse_lecture(cursor, crowdcount, seats_occupied)
                conn.commit()
                seats_occupied = defaultdict(list)
                crowdcounts = []

            next_lecture_ts = DatabaseHandler.get_next_lecture_ts(timestamp)
            curr_lecture = DatabaseHandler.get_lecture_by_ts(timestamp)
        


        if curr_lecture:

            crowdcounts.append(df["crowdcount"].iloc[i])

            cursor.execute("SELECT * FROM seats WHERE occupency_id = ?", (int(df["id"].iloc[i]),))
            result = cursor.fetchall()
            for seat in result:
                seats_occupied[seat[2]].append((timestamp, seat[1], seat[3], seat[4]))
            

# Filter by average crowd count and sum of model confidence