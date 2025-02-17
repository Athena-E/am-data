import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def parse_seat_coords():
    floorplan_file_path = "../data/floorplan_space_ALL.json"
    with open(floorplan_file_path, "r") as file:
        data = json.load(file)
    w, h = data["input_image"]["width"], data["input_image"]["height"]
    seats = data["seats"]
    return w, h, seats

def overlay_seat_ids(seats):
    # overlay seating plan image with seat ids from sensor_locations.json
    seat_floorplan_path = "../imgs/LT1_seating_uncompressed.png"
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
    image.save("annotated_seating_plan.jpg")
    

def seat_to_wgb_coords():
    # LT1 seating XY to WGB (xyzf)
    # approximate
    pass

if __name__ == "__main__":
    w,h,seats = parse_seat_coords()
    # print(seats)
    overlay_seat_ids(seats)
