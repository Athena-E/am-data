from db.utils import get_db
import sys

#* Run ```python view_table.py <table name>```
def display_table(table_name):
    # display all records in table
    db = get_db()

    cursor = db.execute(f"SELECT * FROM {table_name}")

    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})

if __name__ == "__main__":
    display_table(sys.argv[1])
