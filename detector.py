import sqlite3
import re

LOG_FILE = "logs/auth.log"

def detect_bruteforce():
    conn = sqlite3.connect("soc_alerts.db")
    cur = conn.cursor()

    failed_pattern = re.compile(
        r"Failed password for (\w+) from ([\d\.]+)"
    )

    attempts = {}

    with open(LOG_FILE, "r") as log:
        for line in log:
            match = failed_pattern.search(line)
            if match:
                user = match.group(1)
                ip = match.group(2)

                key = (ip, user)
                attempts[key] = attempts.get(key, 0) + 1

    for (ip, user), count in attempts.items():
        if count >= 3:
            if count >= 5:
                severity = "HIGH"
                action = "BLOCK IP"
            else:
                severity = "MEDIUM"
                action = "MONITOR"

            cur.execute("""
                INSERT INTO alerts (ip, username, attempts, severity, action)
                VALUES (?, ?, ?, ?, ?)
            """, (ip, user, count, severity, action))

    conn.commit()
    conn.close()

    print("Detection completed")

if __name__ == "__main__":
    detect_bruteforce()
