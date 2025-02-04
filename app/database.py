import sqlite3
from flask import g
import os
from app.config import Config

DATABASE = Config.DATABASE_PATH

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        with open("../scripts/schema.sql") as f: # AE - modified to relative path
            conn.executescript(f.read())
        conn.close()
