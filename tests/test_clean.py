import unittest
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Prevents from displaying plots during testing
from scripts.clean_data.clean import vectorized_kalman


class TestCleanFunctions(unittest.TestCase):

    def test_vectorized_kalman(self):
        # Arrange
        values = np.array([1, 5, 3, 2, 4])
        time_deltas = np.array([1, 1, 1, 1, 1])
        variance = 1.0

        expected_output = np.array([1, 4, 3, 2, 3])

        # Act
        smoothed_values = vectorized_kalman(values, time_deltas, variance)

        # Assert
        np.testing.assert_array_almost_equal(
            smoothed_values, expected_output, decimal=5
        )


if __name__ == "__main__":
    unittest.main()
