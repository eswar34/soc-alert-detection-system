import sqlite3

conn = sqlite3.connect("soc_alerts.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    username TEXT,
    attempts INTEGER,
    severity TEXT,
    action TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized")
