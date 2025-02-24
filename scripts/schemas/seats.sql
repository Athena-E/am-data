CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    occupency_id INTEGER NOT NULL,  
    seat TEXT NOT NULL,
    seat_confidence REAL NOT NULL,
    model_confidence REAL NOT NULL,
    FOREIGN KEY (occupency_id) REFERENCES occupency(id) ON DELETE CASCADE
);
