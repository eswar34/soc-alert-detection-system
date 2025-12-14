from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_alerts():
    conn = sqlite3.connect("soc_alerts.db")
    cur = conn.cursor()
    cur.execute("SELECT ip, username, attempts, severity, action FROM alerts")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def dashboard():
    alerts = get_alerts()
    return render_template("alerts.html", alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)
