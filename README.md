# 🚀 Volatile Raccoon 🔥

## 📜 Overview 🎯

This project is a Flask-based web application that integrates an SQLite database and data analysis tools. It provides APIs for retrieving sensor data, visualizing trends, and performing analytics. 📊📡

## 🌟 Features 💡

- Flask backend with REST API
- SQLite database for sensor data storage
- Data processing and analysis using Pandas & NumPy
- Modular structure for scalability
- Basic web UI (if applicable)

## 🛠️ Setup Instructions ⚙️

### 1️⃣ Clone the Repository 🖥️

```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2️⃣ Set Up a Virtual Environment (Python 3) 🐍

```sh
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies 📦

```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables 🌍

Create a `.env` file in the root directory:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///data/database.db
```

### 5️⃣ Initialize the Database 🗄️

```sh
python scripts/init_db.py
```

### 6️⃣ Run the Flask App 🚀

```sh
flask run
```

By default, the app will be accessible at `http://127.0.0.1:5000/`. 🌍

## 📂 Directory Structure 🏗️

```
/AM-DATA
│── /app              # Flask application
│   ├── /static       # Frontend assets
│   ├── /templates    # HTML templates
│   ├── /routes       # Flask route handlers
│   ├── /models       # Database models
│   ├── /services     # Business logic & data processing
│   ├── config.py     # Config settings
│── /data             # Database & raw sensor data
│── /scripts          # Utility scripts (DB init, data import)
│── .env              # Environment variables
│── requirements.txt   # Dependencies
│── run.py            # Flask entry point
│── README.md         # This file
```

---
