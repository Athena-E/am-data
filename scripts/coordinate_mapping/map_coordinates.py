import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def parse_seat_coords():
    floorplan_file_path = "data/floorplan_space_ALL.json"
    with open(floorplan_file_path, "r") as file:
        data = json.load(file)
    w, h = data["input_image"]["width"], data["input_image"]["height"]
    seats = data["seats"]
    return w, h, seats

def overlay_seat_ids(seats):
    # overlay seating plan image with seat ids from sensor_locations.json
    seat_floorplan_path = "imgs/LT1_seating_uncompressed.png"
    image = Image.open(seat_floorplan_path)
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()
    font = ImageFont.truetype("Hack-Regular.ttf", 40)
    
    for seat in seats.values():
        x, y, seat_id = seat["x"], seat["y"], seat["seat_id"]
        bbox = draw.textbbox((0, 0), seat_id, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width//2, y), seat_id, fill="red", font=font)

    image = image.convert("RGB")
    image.save("scripts/coordinate_mapping/annotated_seating_plan.jpg")

def transform_coord_system(source_points, dest_points):
    A, _, _, _ = np.linalg.lstsq(source_points, dest_points, rcond=None)

    affine_matrix = np.vstack([A.T, [0, 0, 1]])
    
    return affine_matrix

def seat_to_wgb_coords(seat_x, seat_y):
    # LT1 image seating XY to WGB (xyzf)
    # (approximate for now)
    # front sensor: 72, 270
    # upper left corner: 144, 384 -> (0, 0)
    # upper right corner: 1, 384 -> (5732, 0)
    # bottom right sensor: 1, 268 -> (5732, 5212)
    # bottom left sensor: 144, 267 -> (0, 5212)
    # image dimensions: [5732, 5212]
    
    source_points = np.array([
    [0, 0, 1],
    [5732, 0, 1],
    [5732, 5212, 1],
    [0, 5212, 1]
    ])

    dest_points = np.array([
    [144, 384],
    [1, 384],
    [1, 268],
    [144, 267]
    ])

    input_coords = np.array([seat_x, seat_y, 1])
    affine_matrix = transform_coord_system(source_points, dest_points)
    wgb_coord = np.dot(affine_matrix, input_coords)

    return wgb_coord[:2]

def wgb_to_seat_coords(wgb_x, wgb_y):
    source_points = np.array([
    [144, 384, 1],
    [1, 384, 1],
    [1, 268, 1],
    [144, 267, 1]
    ])

    dest_points = np.array([
    [0, 0],
    [5732, 0],
    [5732, 5212],
    [0, 5212]
    ])

    input_coords = np.array([wgb_x, wgb_y, 1])
    affine_matrix = transform_coord_system(source_points, dest_points)
    seat_coord = np.dot(affine_matrix, input_coords)

    return seat_coord[:2]


if __name__ == "__main__":
    w,h,seats = parse_seat_coords()
    print(w, h)
    overlay_seat_ids(seats)
    print(seat_to_wgb_coords(2866,2606))
