import sqlite3

DATABASE = "./data/database.db"

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return db

def close_db(db):
    db.close()

def init_db():
    conn = sqlite3.connect(DATABASE)
    with open("./scripts/schema.sql") as f: # AE - modified to relative path
        conn.executescript(f.read())
    conn.close()
        
