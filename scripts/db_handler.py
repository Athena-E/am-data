import sqlite3
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
# from app.database import get_db
from app.config import Config

DATABASE = Config.DATABASE_PATH

class DatabaseHandler:

    def __init__(self) -> None:
        self.preprocessed_tbl = "sensor_data"

    def get_all_preprocessed(self):
        app = create_app()
        with app.app_context():
            conn = sqlite3.connect(DATABASE)
            df = pd.read_sql_query(f"SELECT * FROM {self.preprocessed_tbl}", conn)
            conn.close()
            print(df)

    def get_by_timestamp(self, timestamp):
        pass

    # read entry function (readable timestamp)

if __name__ == "__main__":
    db_handler = DatabaseHandler()
    db_handler.get_all_preprocessed()
