from scripts.db.utils import get_db
import os
import json


def parse(raw):
    data = json.loads(raw)
    payload = {
        "crowd_count": data["payload_cooked"]["crowdcount"],
        "occupency_filled": data["payload_cooked"]["occupency_filled"],
        "timestamp": data["acp_ts"],
    }
    payload["seats"] = payload["payload_cooked"]["seats_occupied"].values()
    return payload

def get_next_file(folder):
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(f):
            yield f
        elif os.path.isdir(path):
            yield from get_next_file(path)

def import_occupency():

    folder = "./data/preprocessed/camera"

    gen = get_next_file(folder)
    conn = get_db()

    for filename in gen:
        with open(filename) as f:
            for line in f.readlines():
                payload = parse(line)

                conn.execute(
                    """
                    INSERT OR REPLACE INTO occupency
                    (crowdcount, occupency_filled, timestamp)
                    VALUES (?, ?, ?)
                    """, (payload["crowd_count"], payload["occupency_filled", "timestamp"])
                )

                ref = conn.lastrowid

                for seat in payload["seats"]:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO seats
                        (seat, occupency_id, seat_confidence, model_confidence)
                        VALUES (?, ?, ?, ?)
                        """,
                        (seat["seat"], ref, seat["seat_confidence"], seat["model_confidence"])
                    )
    
    conn.commit()
    conn.close()

