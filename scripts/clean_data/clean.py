import pandas as pd
import numpy as np
from joblib import Parallel, delayed

from ..db_handler import DatabaseHandler
from .kalman_filter import SingleValueKalmanFilter

def vectorized_kalman(values, time_deltas, variance):
    """
    Apply the SingleValueKalmanFilter on a sequence of values with given time deltas.
    
    Args:
        values (array-like): The raw data values to be smoothed.
        time_deltas (array-like): Time differences between consecutive measurements.
        variance (float): Variance for the Kalman filter.

    Returns:
        np.ndarray: Smoothed values.
    """
    kf = SingleValueKalmanFilter(initial=values[0], variance=variance)
    smoothed_values = np.zeros_like(values)

    for i in range(len(values)):
        dt = time_deltas[i] if i > 0 else 1  # Use 1 as the default dt for the first value
        smoothed_values[i] = kf.update(values[i], dt)

    # print(smoothed_values[-10:])
    return smoothed_values

def process_group(group, col, variance):
    """
    Apply a Kalman filter using vectorized_kalman to smooth the specified column in the group.
    """
    values = group[col].values
    time_deltas = group['timestamp'].diff().dt.total_seconds().fillna(1).values  # Time differences in seconds
    group[col] = vectorized_kalman(values, time_deltas, variance)
    return group

import matplotlib.pyplot as plt

def plot_sensor_data(df, sensor_id, day, col='co2'):
    """
    Plots the specified column of data for a single sensor on a given day.
    
    Args:
        df (pd.DataFrame): The DataFrame containing sensor data.
        sensor_id (int or str): The ID of the sensor to plot.
        day (str): The date to filter the data (format: 'YYYY-MM-DD').
        col (str): The column to plot (default: 'CO2').
    """
    # Filter for the selected sensor and date
    df_filtered = df[(df['sensor_id'] == sensor_id) & (df['date_group'].dt.strftime('%Y-%m-%d') == day)]
    
    if df_filtered.empty:
        print(f"No data found for sensor {sensor_id} on {day}.")
        return
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['timestamp'], df_filtered[col], marker='o', linestyle='-', color='royalblue', label=col)

    plt.title(f"{col} Levels for Sensor {sensor_id} on {day}", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel(f"{col} Level", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Set x-axis limits to display only the specific day
    print(df_filtered['timestamp'].max())
    plt.xlim(df_filtered['timestamp'].min(), df_filtered['timestamp'].max())

    # Optionally, format the x-axis to show just the time of day (if the data includes time)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

    plt.tight_layout()
    plt.show()



def clean():

    df = DatabaseHandler.get_all_preprocessed()
    
    VARIANCE = 10

    df['timestamp'] = pd.to_numeric(df['timestamp'])

    df['timestamp'] = pd.to_datetime(pd.to_numeric(df['timestamp']), unit='s')
    df['date_group'] = (
        (df['timestamp'] - pd.to_timedelta(6, unit='h')).dt.floor('24h') + pd.to_timedelta(6, unit='h')
    )

    groups = [group for _, group in df.groupby(['sensor_id', 'date_group'])]

    plot_sensor_data(df, '0520a5', '2025-01-20')

    # group = process_group(groups[1], 'co2', VARIANCE)
    df['new_co2'] = df['co2'].ewm(span=20, adjust=False).mean()

    # print("Original Values:", groups[1][-10:])  # Print the first few values

    plot_sensor_data(df, '0520a5', '2025-01-20', col='new_co2')

    # result = Parallel(n_jobs=-1)(
    #     delayed(process_group)(group, 'co2', variance=VARIANCE) for group in groups
    # )

    # final_df = pd.concat(result, ignore_index=True)

    # plot_sensor_data(final_df, '0520a5', '2025-01-20')



if __name__ == "__main__":
    clean()