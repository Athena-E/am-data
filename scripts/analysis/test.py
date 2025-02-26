from ..db_handler import DatabaseHandler, DATABASE
from .visualisations.view_day import plot_sensor_data
from .utils.calculus import differentiate

import pandas as pd
import sqlite3


TEST_DATE = '2025-02-07'


def analyse_lecture(seats_occupied):
    possible_seats = {seat["seat"] for seat in seats_occupied}
    print(len(possible_seats))

def test():

    df = DatabaseHandler.get_all('occupency')

    df[df["timestamp"] > 1738886400]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"""
            SELECT * FROM seats WHERE occupency_id = ?
            """

    seats_occupied = []

    in_lecture = False
    for i in df.index:


        if in_lecture:

            seats_occupied.append(cursor.execute(query, df["id"].iloc[i]))
            print(len(seats_occupied))

            if in_lecture != DatabaseHandler.get_lecture_by_ts(df["timestamp"].iloc[i]):
                in_lecture = False
                analyse_lecture()
                seats_occupied = []
                return

        else:
            in_lecture = DatabaseHandler.get_lecture_by_ts(df["timestamp"].iloc[i])
            print(df["timestamp"].iloc[i])
            if in_lecture:
                print(in_lecture)


