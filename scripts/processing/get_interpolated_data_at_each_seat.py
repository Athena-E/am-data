from typing import List, Dict
from scripts.coordinate_mapping.map_coordinates import get_seat_coordinates_in_wgb as get_seat_coordinates
from scripts.processing.interpolate_sensor_data import interpolate_sensor_data

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
        - temperature, humidity, co2: The interpolated sensor values
    """
    # Get all seat coordinates
    seat_coordinates = get_seat_coordinates()
    # Convert seat coordinates to format needed for interpolation
    locations = list(seat_coordinates.values())

    # print(locations)
    
    # Get interpolated data for all locations
    # interpolated_data = interpolate_sensor_data(locations, timestamp)
    interpolated_data = interpolate_sensor_data(locations, timestamp)
    
    # Combine seat information with interpolated data
    result = []
    for seat, interp_data in zip(seat_coordinates.values(), interpolated_data):
        result.append({
            'x': seat[0],
            'y': seat[1],
            **interp_data  # This adds temperature, humidity, co2, and zf
        })
    
    return result
