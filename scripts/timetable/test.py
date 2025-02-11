from icalendar import Calendar
import requests 
from datetime import datetime
from pathlib import Path

def parse_ical(ics_path):
    ics = Path(ics_path)
    with ics.open() as f:
        cal = Calendar.from_ical(f.read())
    events = []

    for event in cal.walk('VEVENT'):
        event_data = {
            "summary": str(event.get("SUMMARY")),
            "start": event.get("DTSTART").dt,  # Convert to datetime
            "end": event.get("DTEND").dt,
            "location": str(event.get("LOCATION")),
            "description": str(event.get("DESCRIPTION")),
            "uid": str(event.get("UID")),
        }
        if event_data["location"] == "LT1":
            events.append(event_data)   

    return events

# {'summary': 'Artificial Intelligence', 'start': datetime.datetime(2025, 5, 28, 11, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'end': datetime.datetime(2025, 5, 28, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'location': 'LT1', 'description': 'Lecture with Dr S Holden', 'uid': '1204379'}

if __name__ == "__main__":
    events = parse_ical("./calendar.ical")
    print(events)
