import unittest
from unittest.mock import patch, MagicMock
from scripts.processing.interpolate_sensor_data import (
    get_sensor_data,
    interpolate_sensor_data,
)
import sqlite3
import pandas as pd


class TestInterpolateSensorData(unittest.TestCase):

    @patch("scripts.processing.interpolate_sensor_data.get_db")
    def test_get_sensor_data(self, mock_get_db):
        # Mock the database connection and cursor
        mock_conn = sqlite3.connect(":memory:")  # Create an in-memory database
        mock_conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        mock_get_db.return_value = mock_conn

        # Define the timestamp for fetching sensor data
        timestamp = 1610000000.0

        base_sensor_data = {
            "sensor_id": "sensor_1",
            "temperature": 22.5,
            "humidity": 45.0,
            "co2": 400,
            "timestamp": timestamp,
        }
        base_sensor_data_2 = {**base_sensor_data, "sensor_id": "sensor_2"}

        # Create a pandas DataFrame for the sensor data
        sensor_data_df = pd.DataFrame(
            [
                {**base_sensor_data, "timestamp": timestamp - 5},
                {**base_sensor_data, "timestamp": timestamp - 3},
                {**base_sensor_data, "timestamp": timestamp + 2},
                {**base_sensor_data, "timestamp": timestamp + 10},
                {**base_sensor_data_2, "timestamp": timestamp - 5},
                {**base_sensor_data_2, "timestamp": timestamp},
            ]
        )
        coordinates_df = pd.DataFrame(
            [
                {"sensor_id": "sensor_1", "x": 1.0, "y": 2.0, "zf": 3.0},
                {"sensor_id": "sensor_2", "x": 4.0, "y": 5.0, "zf": 6.0},
            ]
        )

        # Add the DataFrame to the in-memory database
        sensor_data_df.to_sql("sensor_data", mock_conn, index=False)
        coordinates_df.to_sql("coordinates", mock_conn, index=False)

        # Call the function to test
        result = get_sensor_data(timestamp)

        # Check if the result is as expected
        expected_result = [
            {
                **base_sensor_data,
                "timestamp": timestamp + 2,
                "x": 1.0,
                "y": 2.0,
                "zf": 3.0,
            },
            {
                **base_sensor_data_2,
                "timestamp": timestamp,
                "x": 4.0,
                "y": 5.0,
                "zf": 6.0,
            },
        ]
        self.maxDiff = 1000
        self.assertCountEqual(result, expected_result)

        mock_conn.close()

    @patch("scripts.processing.interpolate_sensor_data.get_sensor_data")
    def test_interpolate_sensor_data(self, mock_get_sensor_data):
        # Mock the data returned by get_sensor_data
        # four sensors with data at the same timestamp, located at the corners of a square
        mock_get_sensor_data.return_value = [
            {
                "sensor_id": "sensor_1",
                "temperature": 22.5,
                "humidity": 45.0,
                "co2": 400,
                "x": 0.0,
                "y": 0.0,
                "zf": 0.0,
                "timestamp": 1610000000.0,
            },
            {
                "sensor_id": "sensor_2",
                "temperature": 23.0,
                "humidity": 50.0,
                "co2": 420,
                "x": 0.0,
                "y": 1.0,
                "zf": 0.0,
                "timestamp": 1610000000.0,
            },
            {
                "sensor_id": "sensor_3",
                "temperature": 22.5,
                "humidity": 45.0,
                "co2": 400,
                "x": 1.0,
                "y": 0.0,
                "zf": 0.0,
                "timestamp": 1610000000.0,
            },
            {
                "sensor_id": "sensor_4",
                "temperature": 23.0,
                "humidity": 50.0,
                "co2": 420,
                "x": 1.0,
                "y": 1.0,
                "zf": 1.0,
                "timestamp": 1610000000.0,
            },
        ]

        # Define the location and timestamp for interpolation
        location = (0.5, 0.5, 0)
        timestamp = 1610000000.0

        # Call the function to test
        result = interpolate_sensor_data(location, timestamp)

        # Check if the result is as expected
        expected_result = {
            "temperature": 22.75,
            "humidity": 47.5,
            "co2": 410.0,
        }
        self.assertAlmostEqual(
            result["temperature"], expected_result["temperature"], places=2
        )
        self.assertAlmostEqual(
            result["humidity"], expected_result["humidity"], places=2
        )
        self.assertAlmostEqual(result["co2"], expected_result["co2"], places=2)


if __name__ == "__main__":
    unittest.main()
