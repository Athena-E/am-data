import unittest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevents from displaying plots during testing
from scripts.clean_data.clean import vectorized_kalman, process_group

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
            'timestamp': pd.date_range(start='2021-01-01', periods=5, freq='min'),
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

if __name__ == "__main__":
    unittest.main()