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
    tables = os.listdir('./scripts/schemas')
    for table in tables:
        with open(f"./scripts/schemas/{table}") as f: # AE - modified to relative path
            conn.executescript(f.read())
    conn.close()
        
