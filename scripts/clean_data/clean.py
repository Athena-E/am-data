import pandas as pd
import numpy as np
from joblib import Parallel, delayed

from ..db_handler import DatabaseHandler
from .kalman_filter import KalmanFilter

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
    kf = KalmanFilter(
        initial_value=values[0],
        measurement_variance=variance
    )
    smoothed_values = np.zeros_like(values)

    for i in range(len(values)):
        dt = time_deltas[i] if i > 0 else 1  # Use 1 as the default dt for the first value
        smoothed_values[i] = kf.update(values[i], dt)['value']
        # print(values[i], smoothed_values[i])
        # if (i == 70):
        #     return;

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

def plot_sensor_data(df, sensor_id, day, col1='co2', col2='temperature'):
    """
    Plots two columns of data for a single sensor on a given day using dual y-axes.
    
    Args:
        df (pd.DataFrame): The DataFrame containing sensor data.
        sensor_id (int or str): The ID of the sensor to plot.
        day (str): The date to filter the data (format: 'YYYY-MM-DD').
        col1 (str): The first column to plot (default: 'co2'), will be on left y-axis
        col2 (str): The second column to plot (default: 'temperature'), will be on right y-axis
    """
    # Filter for the selected sensor and date
    df_filtered = df[(df['sensor_id'] == sensor_id) & 
                    (df['date_group'].dt.strftime('%Y-%m-%d') == day)]
    
    if df_filtered.empty:
        print(f"No data found for sensor {sensor_id} on {day}.")
        return
    
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot first column on primary y-axis
    color1 = 'royalblue'
    ax1.set_xlabel("Time", fontsize=12)
    ax1.set_ylabel(col1, color=color1, fontsize=12)
    line1 = ax1.plot(df_filtered['timestamp'], df_filtered[col1], 
                     color=color1, label=col1)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Create secondary y-axis and plot second column
    ax2 = ax1.twinx()
    color2 = 'darkred'
    ax2.set_ylabel(col2, color=color2, fontsize=12)
    line2 = ax2.plot(df_filtered['timestamp'], df_filtered[col2], 
                     color=color2, label=col2)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Add title
    plt.title(f"{col1} and {col2} for Sensor {sensor_id} on {day}", 
              fontsize=14, pad=20)
    
    # Combine legends from both axes
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')
    
    # Set x-axis limits and format
    plt.xlim(df_filtered['timestamp'].min(), df_filtered['timestamp'].max())
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    
    # Add grid but only for the primary axis
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    plt.show()



def clean():

    df = DatabaseHandler.get_all_preprocessed()
    
    VARIANCE = 100

    df['timestamp'] = pd.to_numeric(df['timestamp'])

    df['timestamp'] = pd.to_datetime(pd.to_numeric(df['timestamp']), unit='s')
    df['date_group'] = (
        (df['timestamp'] - pd.to_timedelta(6, unit='h')).dt.floor('24h') + pd.to_timedelta(6, unit='h')
    )

    groups = [group for _, group in df.groupby(['sensor_id', 'date_group'])]

    for sense in ['co2', 'humidity', 'temperature']:

        # print("Original Values:", groups[1][-10:])  # Print the first few values


        for i in range(1):
            groups = Parallel(n_jobs=-1)(
                delayed(process_group)(group, sense, variance=VARIANCE) for group in groups
            )


        final_df = pd.concat(groups, ignore_index=True)
        df[f'new_{sense}'] = final_df[sense]
        # plot_sensor_data(df, '0520a5', '2025-01-20', col1='co2', col2='new_co2')
    
    # df['clean_co2'] = df['co2'].ewm(span=20, adjust=False).mean()
    # df['clean_temperature'] = df['temperature'].ewm(span=20, adjust=False).mean()
    # df['clean_humidity'] = df['humidity'].ewm(span=20, adjust=False).mean()



if __name__ == "__main__":
    clean()