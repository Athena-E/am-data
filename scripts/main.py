from scripts.db.utils import init_db
from scripts.data_loader.import_sensor_data import import_sensor_data
from scripts.data_loader.import_coordinates import import_coordinates
from scripts.data_loader.import_timetable_data import import_timetable
from scripts.clean_data.clean import clean
from scripts.data_loader.import_occupency import import_occupency

from scripts.analysis.test import test

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--add-db", help="Add database?", action=argparse.BooleanOptionalAction)
parser.add_argument("--clean-data", help="Clean Database?", action=argparse.BooleanOptionalAction)

args = parser.parse_args()


#* Run ```python -m scripts.main --add-db --clean-data```
def main():
    
    if (args.add_db):

        init_db()
        print("Database Initialised!")

        import_sensor_data()
        print("Data Imported!")

        import_coordinates()
        print("Coordinates Imported!")

        import_timetable()
        print("Timetable imported!")

        import_occupency()
        print("Occupency Imported")

    if (args.clean_data):
        clean()
        print("Data Cleaned!")

    test()
    



if __name__ == "__main__":
    main()
