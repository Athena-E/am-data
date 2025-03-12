import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.db.utils import get_db, close_db


class DatabaseHandler:

    preprocessed_tbl = "sensor_data"

    @staticmethod
    def get_all(table):
        # return all database data as data frame
        db = get_db()
        df = pd.read_sql_query(f"SELECT * FROM {table}", db)
        close_db(db)
        return df

    @staticmethod
    def get_by_ts_id(timestamp, sensor_id):
        # return record by timestamp and sensor id as a data frame
        db = get_db()
        query = "SELECT * FROM sensor_data WHERE timestamp = ? AND sensor_id = ?"
        df = pd.read_sql_query(query, db, params=(timestamp, sensor_id))
        close_db(db)
        return df

    @staticmethod
    def update_clean_db(table, df, *new_cols):
        db = get_db()
        cursor = db.cursor()

        # Prepare the column names and placeholders for the SQL query
        columns_str = ", ".join(new_cols)  # Convert columns to a comma-separated string
        placeholders = ", ".join(
            "?" for _ in new_cols
        )  # Create ? placeholders for each column

        for index, row in df.iterrows():
            values = tuple(
                row[col] for col in new_cols
            )  # Extract values for the specified columns
            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {table} ({columns_str})
                VALUES ({placeholders})
                """,
                values,
            )

        db.commit()
        close_db(db)

    @staticmethod
    def get_lecture_by_ts(timestamp):
        # get lecture name from current timestamp
        db = get_db()
        cursor = db.execute(
            "SELECT uid, lecture_name, start, end FROM timetable WHERE ? BETWEEN start AND end",
            (timestamp,),
        )
        data = cursor.fetchone()
        close_db(db)

        return data[1] if data else None

    @staticmethod
    def get_next_lecture_ts(timestamp):
        db = get_db()
        cursor = db.execute(
            "SELECT end FROM timetable WHERE ? BETWEEN start AND end", (timestamp,)
        )
        data = cursor.fetchone()

        if data:
            end_time = data[0]
            close_db(db)
            return end_time

        cursor = db.execute(
            "SELECT start FROM timetable WHERE start > ? ORDER BY start ASC LIMIT 1",
            (timestamp,),
        )
        next_lecture = cursor.fetchone()
        close_db(db)

        return next_lecture[0] if next_lecture else None


if __name__ == "__main__":
    db_handler = DatabaseHandler()
