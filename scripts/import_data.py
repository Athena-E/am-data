import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.db_insert_data import insert_list_sensor_data
from scripts.data_loader import get_day_data

if __name__ == "__main__":
    # Add data to the database from preprocessed folder
    
    PREPROCESSED_DIR = '../data/preprocessed'

    # get all preprocessed day data files
    data_files = [f for f in os.listdir(PREPROCESSED_DIR) if os.path.isfile(os.path.join(PREPROCESSED_DIR, f))]

    all_extracted = []
    for f in data_files:
        all_extracted += get_day_data(f)

    insert_list_sensor_data(all_extracted)
    print("Records inserted")
