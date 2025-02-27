CREATE TABLE IF NOT EXISTS clean_seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    occupency_id INTEGER NOT NULL,  
    seat TEXT NOT NULL,
    engagement TEXT NOT NULL,
    FOREIGN KEY (occupency_id) REFERENCES occupency(id) ON DELETE CASCADE
);
