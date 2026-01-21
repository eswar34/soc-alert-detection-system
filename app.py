from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
from collections import Counter
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

def get_alerts():
    conn = sqlite3.connect("soc_alerts.db")
    cur = conn.cursor()
    cur.execute("SELECT ip, username, attempts, severity, action, timestamp FROM alerts ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_alert_stats():
    alerts = get_alerts()
    total = len(alerts)
    severity_counts = Counter(a[3] for a in alerts)
    high = severity_counts.get('HIGH', 0)
    medium = severity_counts.get('MEDIUM', 0)
    low = severity_counts.get('LOW', 0)
    return {
        'total': total,
        'high': high,
        'medium': medium,
        'low': low
    }

@app.route("/")
def dashboard():
    alerts = get_alerts()
    stats = get_alert_stats()
    return render_template("cyber_alerts.html", alerts=alerts, stats=stats)

@app.route("/clear_alerts", methods=['POST'])
def clear_alerts():
    try:
        conn = sqlite3.connect("soc_alerts.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM alerts")
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('initial_data', {
        'alerts': get_alerts(),
        'stats': get_alert_stats()
    })

@socketio.on('request_update')
def handle_update():
    emit('data_update', {
        'alerts': get_alerts(),
        'stats': get_alert_stats()
    })

def background_monitor():
    """Monitor for new alerts and emit updates"""
    last_count = len(get_alerts())
    while True:
        time.sleep(5)  # Check every 5 seconds
        current_count = len(get_alerts())
        if current_count != last_count:
            socketio.emit('data_update', {
                'alerts': get_alerts(),
                'stats': get_alert_stats()
            })
            last_count = current_count

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=9999)
