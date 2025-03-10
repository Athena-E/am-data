from icalendar import Calendar
from dateutil import parser
from pathlib import Path
import json

ICAL_PATH = "./scripts/timetable/calendar.ical"
TIMETABLE_JSON = "./scripts/timetable/timetable.json"


def parse_ical(ics_path):
    ics = Path(ics_path)
    with ics.open() as f:
        cal = Calendar.from_ical(f.read())
    events = []

    for event in cal.walk("VEVENT"):
        start_iso = event.get("DTSTART").dt.isoformat()
        end_iso = event.get("DTEND").dt.isoformat()
        start_dt = parser.isoparse(start_iso)
        end_dt = parser.isoparse(end_iso)
        event_data = {
            "summary": str(event.get("SUMMARY")),
            "start": int(start_dt.timestamp()),
            "end": int(end_dt.timestamp()),
            "location": str(event.get("LOCATION")),
            "description": str(event.get("DESCRIPTION")),
            "uid": str(event.get("UID")),
        }
        if event_data["location"] == "LT1":
            events.append(event_data)

    return events


def load_timetable():
    data = parse_ical(ICAL_PATH)
    return data


def save_to_json(events, filename=TIMETABLE_JSON):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4)


if __name__ == "__main__":
    events = parse_ical(ICAL_PATH)
    save_to_json(events)
    print("Saved LT1 lecture timetable to JSON")
