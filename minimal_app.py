from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_alerts():
    try:
        conn = sqlite3.connect('soc_alerts.db')
        cur = conn.cursor()
        cur.execute('SELECT ip, username, attempts, severity, action, timestamp FROM alerts ORDER BY timestamp DESC')
        rows = cur.fetchall()
        conn.close()
        return rows
    except:
        return []

@app.route('/')
def dashboard():
    return '''
    <h1>SOC Alert Detection System</h1>
    <p>System is running!</p>
    <p><a href="/api/alerts">View API</a></p>
    '''

@app.route('/api/alerts')
def api_alerts():
    alerts = get_alerts()
    return jsonify([{'ip': row[0], 'user': row[1], 'attempts': row[2], 'severity': row[3]} for row in alerts])

@app.route('/api/system-health')
def system_health():
    return jsonify({'cpu': 45, 'memory': 60, 'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
