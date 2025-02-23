import os

from scripts.db.insert_data import insert_list_sensor_data
from scripts.data_loader.load_sensor_data import get_day_data

# calls methods to load and insert sensor data

def import_sensor_data():
    # Add all data to the database from preprocessed folder
    
    PREPROCESSED_DIR = './data/preprocessed'

    # get all preprocessed day data files
    data_files = [f for f in os.listdir(PREPROCESSED_DIR) if os.path.isfile(os.path.join(PREPROCESSED_DIR, f))]

    all_extracted = []
    for f in data_files:
        all_extracted += get_day_data(f)
    
    insert_list_sensor_data(all_extracted)
