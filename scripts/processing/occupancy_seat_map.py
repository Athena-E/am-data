import json
from scripts.db.utils import get_db

# 07/02/25: [1738886400, 1738972800]

def get_occupancy_seat_map(ts):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("select id, crowdcount, timestamp from occupency where timestamp >= 1738938183.35689 and timestamp <= 1738972800;")
    occupancy_recs = cursor.fetchall()

    occupancy_map = {}

    for occupancy_id, crowdcount, timestamp in occupancy_recs:
        cursor.execute("""
            SELECT seat, engagement 
            FROM clean_seats 
            WHERE occupency_id = ?;
        """, (occupancy_id,))
        seat_data = cursor.fetchall()

        seats_occupied = [
            {"seat_id": seat_id, "engagement": engagement}
            for seat_id, engagement in seat_data
        ]

        occupancy_map[timestamp] = {
            "crowdcount": crowdcount,
            "seats_occupied": seats_occupied
        }

    return occupancy_map

def save_to_json(map, filename="./scripts/processing/occupancy_seat_map_0702.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(map, f, indent=4)

if __name__ == "__main__":
    timestamp = 1738938185.49893  
    occupancy_seat_map = get_occupancy_seat_map(timestamp)
    save_to_json(occupancy_seat_map)
    print("saved to json!")

# {
#     "<timestamp>": {
#         "crowdcount": 55,
#         "seats_occupied": [
#             {
#                 "seat_id": "M45",
#                 "engagement": "LOW"
#             }
#         ]
#     }
# }
#
# SELECT id, crowdcount, timestamp FROM occupency;
# SELECT seat_id, engagement FROM clean_seat_data WHERE id = occupency_id;
