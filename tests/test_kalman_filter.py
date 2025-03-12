import unittest
from scripts.clean_data.kalman_filter import KalmanFilter


class TestKalmanFilter(unittest.TestCase):

    def test_initialization(self):
        # Test the initialization of the Kalman filter
        initial_value = 10.0
        variance = 0.5
        kf = KalmanFilter(initial_value=initial_value, measurement_variance=variance)

        self.assertEqual(kf.x[0, 0], initial_value)
        self.assertEqual(kf.x[1, 0], 0.0)
        self.assertEqual(kf.P[0, 0], 1000.0)
        self.assertEqual(kf.P[1, 1], 1000.0)
        self.assertEqual(kf.R[0, 0], variance)
        self.assertEqual(kf.H[0, 0], 1.0)
        self.assertEqual(kf.H[0, 1], 0.0)

    def test_update(self):
        # Test the update method of the Kalman filter
        initial_value = 0.0
        variance = 0.1
        kf = KalmanFilter(initial_value=initial_value, measurement_variance=variance)

        measured_value = 5.0
        dt = 1.0
        filtered_value = kf.update(measured_value, dt)["value"]

        # TODO: Check if the filtered value is within a reasonable range
        self.assertTrue(0.0 <= filtered_value <= 5.0)

    def test_update_with_no_change(self):
        # Test the update method with no change in measured value
        initial_value = 10.0
        variance = 0.1
        kf = KalmanFilter(initial_value=initial_value, measurement_variance=variance)

        measured_value = 10.0
        dt = 1.0
        filtered_value = kf.update(measured_value, dt)["value"]

        # TODO: Check if the filtered value is close to the measured value
        self.assertAlmostEqual(filtered_value, measured_value, places=1)


if __name__ == "__main__":
    unittest.main()
