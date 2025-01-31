

#* Initialise Database
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import init_db

if __name__ == "__main__":
    init_db()
    print("Database initialized!")
    
