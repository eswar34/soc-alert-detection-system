import sqlite3
from datetime import datetime

conn = sqlite3.connect("soc_alerts.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    username TEXT,
    attempts INTEGER,
    severity TEXT,
    action TEXT,
    timestamp TEXT DEFAULT (datetime('now'))
)
""")

conn.commit()
conn.close()

print("Database initialized")
