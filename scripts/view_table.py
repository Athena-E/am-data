from scripts.db.utils import get_db


def display_table():
    # display all records in sensor_table
    db = get_db()

    print("sensor data:")

    cursor = db.execute("SELECT * FROM sensor_data")

    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})

    print("coordinates:")

    cursor = db.execute("SELECT * FROM coordinates")

    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})


if __name__ == "__main__":
    display_table()
