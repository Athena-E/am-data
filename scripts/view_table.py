import sqlite3
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.database import DATABASE

def display_table():
    # display all records in sensor_table
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print('sensor data:')
    
    cursor.execute("SELECT * FROM sensor_data")
    
    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})
    
    print('coordinates:')

    cursor.execute("SELECT * FROM coordinates")

    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})

    conn.close()

if __name__ == "__main__":
    display_table()
