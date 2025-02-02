import sqlite3

# Create a fake database with a table named sensor_data
# Its schema should be (timestamp, temperature, humidity, co2)

# Connect to the SQLite database
conn = sqlite3.connect('fake.db')

# Create a cursor object using the connection
cursor = conn.cursor()

# Drop the sensor_data table if it already exists
cursor.execute('DROP TABLE IF EXISTS sensor_data')

# Create a table named sensor_data with the specified schema
cursor.execute('''CREATE TABLE sensor_data (
                    timestamp TEXT,
                    temperature REAL,
                    humidity REAL,
                    co2 REAL
                )''')

# Insert some sample data into the sensor_data table
data = [
    ('2021-01-01 12:00:00', 25.0, 50.0, 400.0),
    ('2021-01-01 12:15:00', 26.0, 51.0, 450.0),
    ('2021-01-01 12:30:00', 27.0, 52.0, 500.0),
    ('2021-01-01 12:55:00', 28.0, 53.0, 550.0),
    ('2021-01-01 12:57:00', 28.0, 53.0, 540.0),
    ('2021-01-01 13:00:00', 29.0, 54.0, 600.0)
]

# Insert the sample data into the sensor_data table
cursor.executemany('INSERT INTO sensor_data VALUES (?, ?, ?, ?)', data)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

