from scripts.db.utils import get_db
from scripts.timetable.get_lecture_times import load_timetable

def import_timetable():
    db = get_db()
    data = load_timetable()

    db.execute("DROP TABLE IF EXISTS timetable")
    db.commit()

    db.execute(
        """
        CREATE TABLE timetable (
            uid INTEGER PRIMARY KEY NOT NULL,
            lecture_name TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL
        )
        """
    )
    db.commit()

    query = """
    INSERT OR REPLACE INTO timetable (uid, lecture_name, start, end)
    VALUES (?, ?, ?, ?)
    """

    records = [
        (time["uid"], time["summary"], time["start"], time["end"])
         for time in data 
         if all(t in time for t in ("uid", "summary", "start", "end"))
    ]

    if records:
        db.executemany(query, records)
        db.commit()
