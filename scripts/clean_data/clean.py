import pandas as pd
import numpy as np
from joblib import Parallel, delayed

from ..utils.db_handler import DatabaseHandler
from .kalman_filter import KalmanFilter
from .particle_filter import ParticleFilter
from ..analysis.visualisations.view_day import plot_sensor_data


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
    kf = KalmanFilter(initial_value=values[0], measurement_variance=variance)
    smoothed_values = np.zeros_like(values)

    for i in range(len(values)):
        dt = (
            time_deltas[i] if i > 0 else 1
        )  # Use 1 as the default dt for the first value
        smoothed_values[i] = kf.update(values[i], dt)["value"]

    return smoothed_values


def vectorized_particle_filter(values, time_deltas, variance):
    """
    Apply the ParticleFilter on a sequence of values with given time deltas.

    Args:
        values (array-like): The raw data values to be smoothed.
        time_deltas (array-like): Time differences between consecutive measurements.
        variance (float): Variance for the Kalman filter.

    Returns:
        np.ndarray: Smoothed values.
    """
    pf = ParticleFilter(
        num_particles=1000,
        process_variance_rate=0.5,
        measurement_variance=variance,
        initial_value=values[0],
    )
    smoothed_values = np.zeros_like(values)

    for i in range(len(values)):
        dt = (
            time_deltas[i] if i > 0 else 1
        )  # Use 1 as the default dt for the first value
        pf.update(values[i], dt)
        smoothed_values[i] = pf.estimate()

    return smoothed_values


def process_group(data_filter, group, col, variance):
    """
    Apply a filter using vectorized_{filter} to smooth the specified column in the group.
    """
    values = group[col].values
    time_deltas = group["timestamp"].diff().fillna(0).values
    group[col] = data_filter(values, time_deltas, variance)
    return group


def clean():

    df = DatabaseHandler.get_all("sensor_data")

    # print(np.var(df['co2'][:100]))

    VARIANCE = 45 * 8

    df["timestamp"] = pd.to_numeric(df["timestamp"])

    df["date_group"] = (
        pd.to_datetime(df["timestamp"], unit="s") - pd.to_timedelta(6, unit="h")
    ).dt.floor("24h") + pd.to_timedelta(6, unit="h")

    # for data_filter in [vectorized_particle_filter, vectorized_kalman]:

    #     groups = [group for _, group in df.groupby(['sensor_id', 'date_group'])]

    #     for sense in ['co2']:

    #         for i in range(1):
    #             groups = Parallel(n_jobs=-1)(
    #                 delayed(process_group)(data_filter, group, sense, variance=VARIANCE) for group in groups
    #             )

    #         final_df = pd.concat(groups, ignore_index=True)
    #         df.loc[:, sense] = final_df[sense]

    # SPAN = 10
    # df['co2'] = df['co2'].ewm(span=SPAN, adjust=False).mean()
    # df['temperature'] = df['temperature'].ewm(span=SPAN, adjust=False).mean()
    # df['humidity'] = df['humidity'].ewm(span=SPAN, adjust=False).mean()

    DatabaseHandler.update_clean_db(
        "clean_sensor_data",
        df,
        "timestamp",
        "sensor_id",
        "co2",
        "temperature",
        "humidity",
        "motion",
    )


if __name__ == "__main__":
    clean()
