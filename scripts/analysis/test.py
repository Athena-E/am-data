from ..db_handler import DatabaseHandler
from .visualisations.view_day import plot_sensor_data
from .utils.calculus import differentiate

import pandas as pd

def test():

    df = DatabaseHandler.get_all('clean_sensor_data')

    df['timestamp'] = pd.to_numeric(df['timestamp'])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['date_group'] = (
        (df['timestamp'] - pd.to_timedelta(6, unit='h')).dt.floor('24h') + pd.to_timedelta(6, unit='h')
    )

    plot_sensor_data(df, '0520a5', '2025-01-20', col1='co2')

    differentiate(df, 'co2', 'timestamp', 'd-co2')

    plot_sensor_data(df, '0520a5', '2025-01-20', col1='d-co2')