import sqlite3

conn = sqlite3.connect("soc_alerts.db")
cur = conn.cursor()

cur.execute("SELECT * FROM alerts")
alerts = cur.fetchall()

with open("incident_report.txt", "w") as f:
    f.write("SOC INCIDENT REPORT\n")
    f.write("===================\n\n")

    for a in alerts:
        f.write(f"IP Address: {a[1]}\n")
        f.write(f"Username: {a[2]}\n")
        f.write(f"Attempts: {a[3]}\n")
        f.write(f"Severity: {a[4]}\n")
        f.write(f"Action Taken: {a[5]}\n")
        f.write("---------------------------\n")

conn.close()
print("Incident report generated")
