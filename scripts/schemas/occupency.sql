CREATE TABLE IF NOT EXISTS occupency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crowdcount INTEGER NOT NULL,
    occupency_filled REAL NOT NULL,
    timestamp REAL NOT NULL
);