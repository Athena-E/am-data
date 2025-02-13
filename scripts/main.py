import os

from app.database import init_db
from scripts.db_insert_data import insert_list_sensor_data

from scripts.data_loader import get_day_data

from scripts.clean_data.clean import clean


import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--add-db", help="Add database?", action=argparse.BooleanOptionalAction)
parser.add_argument("--clean-data", help="Clean Database?", action=argparse.BooleanOptionalAction)

args = parser.parse_args()


def main():
    
    if (args.add_db):

        init_db()
        print("Database Initialise!")

        PREPROCESSED_DIR = './data/preprocessed'

        # get all preprocessed day data files
        data_files = [f for f in os.listdir(PREPROCESSED_DIR) if os.path.isfile(os.path.join(PREPROCESSED_DIR, f))]

        all_extracted = []
        for f in data_files:
            all_extracted += get_day_data(f)

        insert_list_sensor_data(all_extracted)
        print("Records inserted")

    if (args.clean_data):
        clean()


if __name__ == "__main__":
    main()
