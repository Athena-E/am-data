from typing import List, Dict
from scripts.coordinate_mapping.map_coordinates import (
    get_seat_coordinates_in_wgb as get_seat_coordinates,
)
from scripts.processing.interpolate_sensor_data import interpolate_sensor_data
from scripts.db.utils import get_db


def get_interpolated_data_at_each_seat(timestamp: float) -> List[Dict]:
    """
    Get interpolated sensor data at each seat location.

    Args:
        timestamp: A float representing the timestamp to get data for.

    Returns:
        A list of dictionaries containing the interpolated sensor data at each seat location.
        Each dictionary contains:
        - seat_id: The ID of the seat
        - x, y: The coordinates of the seat
        - temperature, humidity, co2, zf: The interpolated sensor values
        - crowdcount: from the occupency data
    """
    db = get_db()

    # Get all seat coordinates
    seat_coordinates = get_seat_coordinates()

    # Convert seat coordinates to format needed for interpolation
    locations = list(seat_coordinates.values())

    # Get interpolated data for all locations
    interpolated_data = interpolate_sensor_data(locations, timestamp)

    # Fetch occupency data
    occupency_data = db.execute(
        """
        WITH ranked_occupency AS (
            SELECT seat, crowdcount, timestamp,
                   ROW_NUMBER() OVER (PARTITION BY seat ORDER BY ABS(timestamp - ?) ASC) AS rank
            FROM occupency
            JOIN seats ON occupency.id = seats.occupency_id
        )
        SELECT seat, crowdcount
        FROM ranked_occupency
        WHERE rank = 1
        """, (timestamp,)
    ).fetchall()
    occupency_dict = {row["seat"]: row["crowdcount"] for row in occupency_data}

    # Combine seat information with interpolated data
    result = []
    for (seat_id, seat), interp_data in zip(
        seat_coordinates.items(), interpolated_data
    ):
        result.append(
            {
                "seat_id": seat_id,
                "x": seat[0],
                "y": seat[1],
                **interp_data,  # This adds temperature, humidity, co2, and zf
                "crowdcount": occupency_dict.get(seat_id, 0),  # Add crowdcount
            }
        )

    return result
