from icalendar import Calendar
import requests 
from datetime import datetime
from pathlib import Path

def parse_ical(ics_path):
    with ics_path.open() as f:
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
        events.append(event_data)

    return events

if __name__ == "__main__":
    events = parse_ical("./calendar.ical")
    print(events)
