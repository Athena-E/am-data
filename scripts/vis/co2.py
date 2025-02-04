import sqlite3
import matplotlib.pyplot as plt

def plot_co2_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('fake.db')
    cursor = conn.cursor()
    
    # Execute a query to fetch timestamp and CO2 data from the sensor_data table
    cursor.execute("SELECT timestamp, co2 FROM sensor_data")
    data = cursor.fetchall()

    # Extract timestamps and CO2 levels from the fetched data
    timestamps = [row[0] for row in data]
    co2_levels = [row[1] for row in data]

    # Create a line plot with the fetched data
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, co2_levels, marker='o', linestyle='-', color='b')
    plt.xlabel('Timestamp')
    plt.ylabel('CO2 Level (ppm)')
    plt.title('CO2 Levels Over Time')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()  # Display the plot

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    plot_co2_data()
