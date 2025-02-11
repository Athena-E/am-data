import sqlite3
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_db
from app.config import Config
from run import app

DATABASE = Config.DATABASE_PATH

class DatabaseHandler:

    preprocessed_tbl = "sensor_data"

    @staticmethod
    def get_all_preprocessed():
        # return all database data as data frame
        with app.app_context():
            conn = sqlite3.connect(DATABASE)
            df = pd.read_sql_query(f"SELECT * FROM {DatabaseHandler.preprocessed_tbl}", conn)
            conn.close()
        return df

    @staticmethod
    def get_by_ts_id(timestamp, sensor_id):
        # return record by timestamp and sensor id as a data frame
        with app.app_context():
            conn = sqlite3.connect(DATABASE)
            # cursor = get_db().cursor()
            # cursor.execute("SELECT * FROM sensor_data WHERE timestamp = ? AND sensor_id = ?", (timestamp, sensor_id))
            df = pd.read_sql_query(f"SELECT * FROM sensor_data WHERE timestamp = {timestamp} AND sensor_id = {sensor_id}", conn)
        return df

    # read entry function (readable timestamp)

if __name__ == "__main__":
    db_handler = DatabaseHandler()
    db_handler.get_all_preprocessed()
    db_handler.get_by_ts_id("1737590422.711448", "0520a5")
