import unittest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevents from displaying plots during testing
from scripts.clean_data.clean import vectorized_kalman, process_group, plot_sensor_data

class TestCleanFunctions(unittest.TestCase):

    def test_vectorized_kalman(self):
        # Sample input data
        values = np.array([1, 2, 3, 4, 5])
        time_deltas = np.array([1, 1, 1, 1, 1])
        variance = 1.0

        # TODO: Expected output (this is just an example, you may need to adjust it based on the actual implementation)
        expected_output = np.array([1, 1.5, 2.25, 3.125, 4.0625])

        # Call the function
        smoothed_values = vectorized_kalman(values, time_deltas, variance)

        # Check if the output is as expected
        np.testing.assert_array_almost_equal(smoothed_values, expected_output, decimal=5)

    def test_process_group(self):
        # Sample input data
        data = {
            'timestamp': pd.date_range(start='2021-01-01', periods=5, freq='T'),
            'co2': [400, 420, 430, 410, 415]
        }
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        group = df.copy()

        # Call the function
        processed_group = process_group(group, 'co2', variance=1.0)

        # Check if the output is as expected
        self.assertEqual(len(processed_group), len(group))
        self.assertTrue('co2' in processed_group.columns)

    def test_plot_sensor_data(self):
        # Sample input data
        data = {
            'timestamp': pd.date_range(start='2021-01-01', periods=5, freq='T'),
            'sensor_id': ['0520a5'] * 5,
            'date_group': pd.date_range(start='2021-01-01', periods=5, freq='T'),
            'co2': [400, 420, 430, 410, 415]
        }
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date_group'] = pd.to_datetime(df['date_group'])

        # Call the function and ensure no exceptions are raised
        try:
            plot_sensor_data(df, '0520a5', '2021-01-01', col='co2')
        except Exception as e:
            self.fail(f"plot_sensor_data raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()