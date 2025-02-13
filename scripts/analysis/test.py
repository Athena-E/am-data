from ..db_handler import DatabaseHandler
from visualisations.view_day import plot_sensor_data
from utils.calculus import differentiate

df = DatabaseHandler.get_all_preprocessed()

plot_sensor_data(df, '0520a5', '2025-01-20', col1='co2', col2='clean-co2')

differentiate(df, 'clean-co2', 'timestamps', 'd-co2')

plot_sensor_data(df, '0520a5', '2025-01-20', col1='d-co2')