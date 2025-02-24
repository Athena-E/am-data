import sqlite3
import os

DATABASE = "./data/database.db"

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return db

def close_db(db):
    db.close()

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    tables = os.listdir('./scripts/schemas')
    for table in tables:
        with open(f"./scripts/schemas/{table}") as f: 
            conn.executescript(f.read())
    conn.close()
        
