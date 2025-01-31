import sqlite3
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import DATABASE

def display_table():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sensor_data")
    
    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})
    
    conn.close()

if __name__ == "__main__":
    display_table()
