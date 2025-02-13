from scripts.db.utils import init_db
from scripts.data_loader.import_sensor_data import import_sensor_data
from scripts.clean_data.clean import clean


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

    if (args.clean_data):
        clean()
        print("Data Cleaned!")


if __name__ == "__main__":
    main()
