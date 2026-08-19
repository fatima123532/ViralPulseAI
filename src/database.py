import sqlite3
import os
import pandas as pd
from datetime import datetime, timezone

DB_PATH = "data/predictions_history.db"

def init_db():
    """Initializes the SQLite database table if it does not exist."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            title TEXT,
            channel TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            velocity REAL,
            prediction INTEGER,
            sentiment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_prediction(video_id, title, channel, views, likes, comments, velocity, prediction, sentiment):
    """Logs a new prediction entry into the historical database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO predictions (video_id, title, channel, views, likes, comments, velocity, prediction, sentiment, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (video_id, title, channel, views, likes, comments, velocity, prediction, sentiment, now_str))
    conn.commit()
    conn.close()

def fetch_prediction_history(limit=50):
    """Fetches historical prediction records as a Pandas DataFrame."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT id, video_id, title, channel, views, velocity, prediction, sentiment, timestamp FROM predictions ORDER BY timestamp DESC LIMIT {limit}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_database_stats():
    """Returns total logs, viral count, and normal count from the database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) FROM predictions")
    row = cursor.fetchone()
    conn.close()
    total = row[0] if row[0] else 0
    viral = row[1] if row[1] else 0
    normal = total - viral
    return {"total": total, "viral": viral, "normal": normal}

if __name__ == "__main__":
    init_db()
    print("Database module initialized successfully.")