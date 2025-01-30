import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DATABASE_PATH = os.getenv("DATABASE_URL", "data/database.db")
