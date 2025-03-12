from ..db.utils import get_db
import sys


def display_table(table_name):
    db = get_db()

    cursor = db.execute(f"SELECT * FROM {table_name}")

    rows = cursor.fetchall()
    for row in rows:
        print({col: row[col] for col in row.keys()})


if __name__ == "__main__":
    display_table(sys.argv[1])
