from scripts.db.utils import get_db
import os
import json
from tqdm import tqdm


def parse(raw):
    data = json.loads(raw)
    payload = {
        "crowd_count": data["payload_cooked"]["crowdcount"],
        "occupency_filled": data["payload_cooked"]["occupancy_filled"],
        "timestamp": data["acp_ts"],
    }
    payload["seats"] = data["payload_cooked"]["seats_occupied"].values()
    return payload


def get_next_file(folder):
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            yield from get_next_file(path)


# Import occupency data from camera data
def import_occupency():
    folder = "./data/preprocessed/camera"

    gen = get_next_file(folder)
    conn = get_db()
    cursor = conn.cursor()

    for filename in tqdm(gen):
        with open(filename) as f:
            for line in f.readlines():
                try:
                    payload = parse(line)

                    assert (
                        all(
                            map(
                                lambda seat: all(
                                    [
                                        "seat_id" in seat,
                                        "seat_confidence" in seat,
                                        "model_confidence" in seat,
                                    ]
                                ),
                                payload["occupency_filled"],
                            )
                        )
                        or len(payload["occupency_filled"]) == 0
                    )

                    assert all(
                        [
                            "crowd_count" in payload,
                            "occupency_filled" in payload,
                            "timestamp" in payload,
                        ]
                    )

                except:
                    pass

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO occupency
                    (crowdcount, occupency_filled, timestamp)
                    VALUES (?, ?, ?)
                    """,
                    (
                        payload["crowd_count"],
                        payload["occupency_filled"],
                        payload["timestamp"],
                    ),
                )

                ref = cursor.lastrowid

                for seat in payload["seats"]:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO seats
                        (seat, occupency_id, seat_confidence, model_confidence)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            seat["seat_id"],
                            ref,
                            seat["seat_confidence"],
                            seat["model_confidence"],
                        ),
                    )

    conn.commit()
    conn.close()
