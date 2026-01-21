from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from collections import Counter
import json
import csv
import io
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
import psutil
import platform
import socket
import subprocess
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'log', 'txt', 'csv', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Email configuration (configure these with your email settings)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@gmail.com'  # Replace with your email
SMTP_PASSWORD = 'your-app-password'     # Replace with app password
ALERT_RECIPIENTS = ['admin@company.com']  # Replace with actual recipients

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Setup logging
logging.basicConfig(filename='soc_alerts.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

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

def get_recent_alerts(limit=5):
    conn = sqlite3.connect("soc_alerts.db")
    cur = conn.cursor()
    cur.execute("SELECT ip, username, attempts, severity, action, timestamp FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_alerts_by_time_range(hours=24):
    conn = sqlite3.connect("soc_alerts.db")
    cur = conn.cursor()
    time_threshold = datetime.now() - timedelta(hours=hours)
    cur.execute("SELECT ip, username, attempts, severity, action, timestamp FROM alerts WHERE timestamp > ? ORDER BY timestamp DESC", (time_threshold,))
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def dashboard():
    alerts = get_alerts()
    stats = get_alert_stats()
    return render_template("cyber_alerts.html", alerts=alerts, stats=stats)

@app.route("/api/alerts")
def api_alerts():
    alerts = get_alerts()
    return jsonify([{
        'ip': a[0],
        'username': a[1],
        'attempts': a[2],
        'severity': a[3],
        'action': a[4],
        'timestamp': a[5]
    } for a in alerts])

@app.route("/api/stats")
def api_stats():
    stats = get_alert_stats()
    return jsonify(stats)

@app.route("/api/recent-activity")
def api_recent_activity():
    alerts = get_recent_alerts(10)
    return jsonify([{
        'ip': a[0],
        'username': a[1],
        'attempts': a[2],
        'severity': a[3],
        'action': a[4],
        'timestamp': a[5]
    } for a in alerts])

@app.route("/run_detector")
def run_detector():
    import subprocess
    try:
        result = subprocess.run([
            r"E:/Dot net full stack development(HCL)/.venv/Scripts/python.exe",
            "detector.py"
        ], cwd=r"e:\Dot net full stack development(HCL)\js\soc-alert-detection-system", capture_output=True, text=True)
        return jsonify({"success": True, "output": result.stdout})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

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

@app.route("/export_alerts")
def export_alerts():
    try:
        alerts = get_alerts()
        format_type = request.args.get('format', 'csv')

        if format_type == 'csv':
            # Create CSV
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'IP Address', 'Username', 'Attempts', 'Severity', 'Action', 'Timestamp'])

            for i, alert in enumerate(alerts, 1):
                writer.writerow([i, alert[0], alert[1], alert[2], alert[3], alert[4], alert[5]])

            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name='soc_alerts_export.csv'
            )

        elif format_type == 'json':
            # Create JSON
            alert_data = [{
                'id': i,
                'ip': alert[0],
                'username': alert[1],
                'attempts': alert[2],
                'severity': alert[3],
                'action': alert[4],
                'timestamp': alert[5]
            } for i, alert in enumerate(alerts, 1)]

            return jsonify({
                'export_date': datetime.now().isoformat(),
                'total_alerts': len(alerts),
                'alerts': alert_data
            })

        else:
            return jsonify({"error": "Unsupported format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/system-health")
def system_health():
    # Mock system health data - in a real SOC, this would come from monitoring tools
    import psutil
    import platform

    try:
        return jsonify({
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
            'system_info': {
                'platform': platform.system(),
                'version': platform.version(),
                'python_version': platform.python_version()
            }
        })
    except ImportError:
        # Fallback if psutil is not available
        return jsonify({
            'cpu_percent': 45,
            'memory_percent': 67,
            'disk_usage': 32,
            'network_connections': 150,
            'system_info': {
                'platform': platform.system(),
                'version': platform.version(),
                'python_version': platform.python_version()
            }
        })

@app.route("/api/alert-details/<int:alert_id>")
def alert_details(alert_id):
    alerts = get_alerts()
    if 1 <= alert_id <= len(alerts):
        alert = alerts[alert_id - 1]
        return jsonify({
            'id': alert_id,
            'ip': alert[0],
            'username': alert[1],
            'attempts': alert[2],
            'severity': alert[3],
            'action': alert[4],
            'timestamp': alert[5],
            'details': {
                'risk_score': calculate_risk_score(alert),
                'similar_alerts': get_similar_alerts(alert[0]),
                'geolocation': get_ip_geolocation(alert[0])  # Mock function
            }
        })
    return jsonify({"error": "Alert not found"}), 404

def calculate_risk_score(alert):
    # Simple risk scoring based on severity and attempts
    base_score = {'HIGH': 100, 'MEDIUM': 50, 'LOW': 25}.get(alert[3], 25)
    attempt_multiplier = min(alert[2] / 5, 3)  # Cap at 3x for attempts > 15
    return int(base_score * attempt_multiplier)

def get_similar_alerts(ip):
    alerts = get_alerts()
    similar = [a for a in alerts if a[0] == ip]
    return len(similar)

def get_ip_geolocation(ip):
    # Mock geolocation - in real implementation, use a geolocation service
    return {
        'country': 'Unknown',
        'city': 'Unknown',
        'coordinates': [0, 0]
    }

# Email alert functions
def send_email_alert(subject, message, recipients=None):
    """Send email alert for security incidents"""
    if not recipients:
        recipients = ALERT_RECIPIENTS

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = f"🚨 SOC ALERT: {subject}"

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, recipients, text)
        server.quit()

        logging.info(f"Email alert sent: {subject}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email alert: {str(e)}")
        return False

def send_system_notification(title, message):
    """Send system notification (Windows toast notification)"""
    try:
        # For Windows systems
        if platform.system() == 'Windows':
            subprocess.run([
                'powershell',
                '-Command',
                f'New-BurntToastNotification -Text "{title}", "{message}" -AppLogo "C:\\Windows\\System32\\SecurityAndMaintenance.png"'
            ], capture_output=True)
        logging.info(f"System notification sent: {title}")
        return True
    except Exception as e:
        logging.error(f"Failed to send system notification: {str(e)}")
        return False

def check_login_limits():
    """Check for login limit violations and send alerts"""
    alerts = get_alerts()
    critical_alerts = [a for a in alerts if a[3] == 'HIGH' and 'FAILED' in str(a[4]).upper()]

    if len(critical_alerts) >= 3:  # Threshold for alerts
        subject = "CRITICAL: Multiple Failed Login Attempts Detected"
        message = f"""
        <h2>🚨 Security Alert: Login Limit Exceeded</h2>
        <p><strong>Alert Count:</strong> {len(critical_alerts)}</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Details:</strong> Multiple failed login attempts detected from various IPs.</p>
        <p>Please investigate immediately.</p>
        """

        send_email_alert(subject, message)
        send_system_notification("SOC Alert", f"{len(critical_alerts)} critical login failures detected!")

# Enhanced system health monitoring
def get_detailed_system_health():
    """Get comprehensive system health metrics"""
    try:
        # CPU details
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # Memory details
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used / (1024**3)  # GB
        memory_total = memory.total / (1024**3)  # GB

        # Disk details
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = disk.used / (1024**3)  # GB
        disk_total = disk.total / (1024**3)  # GB

        # Network details
        network = psutil.net_io_counters()
        bytes_sent = network.bytes_sent / (1024**2)  # MB
        bytes_recv = network.bytes_recv / (1024**2)  # MB
        network_connections = len(psutil.net_connections())

        # System info
        system_info = {
            'platform': platform.system(),
            'version': platform.version(),
            'hostname': socket.gethostname(),
            'python_version': platform.python_version(),
            'uptime': get_system_uptime()
        }

        # Process monitoring
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort by CPU usage and take top 10
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = processes[:10]

        return {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency': cpu_freq.current if cpu_freq else 0
            },
            'memory': {
                'percent': memory_percent,
                'used_gb': round(memory_used, 2),
                'total_gb': round(memory_total, 2)
            },
            'disk': {
                'percent': disk_percent,
                'used_gb': round(disk_used, 2),
                'total_gb': round(disk_total, 2)
            },
            'network': {
                'bytes_sent_mb': round(bytes_sent, 2),
                'bytes_recv_mb': round(bytes_recv, 2),
                'connections': network_connections
            },
            'system_info': system_info,
            'top_processes': top_processes,
            'health_score': calculate_health_score(cpu_percent, memory_percent, disk_percent)
        }
    except Exception as e:
        logging.error(f"Error getting system health: {str(e)}")
        return {
            'error': str(e),
            'cpu': {'percent': 0},
            'memory': {'percent': 0},
            'disk': {'percent': 0},
            'network': {'connections': 0},
            'system_info': {},
            'top_processes': [],
            'health_score': 0
        }

def get_system_uptime():
    """Get system uptime"""
    try:
        uptime_seconds = psutil.boot_time()
        uptime = datetime.now() - datetime.fromtimestamp(uptime_seconds)
        return str(uptime).split('.')[0]  # Remove microseconds
    except:
        return "Unknown"

def calculate_health_score(cpu_percent, memory_percent, disk_percent):
    """Calculate overall system health score (0-100)"""
    # Lower percentages are better for CPU, memory, disk usage
    cpu_score = max(0, 100 - cpu_percent)
    memory_score = max(0, 100 - memory_percent)
    disk_score = max(0, 100 - disk_percent)

    # Weighted average (CPU 40%, Memory 40%, Disk 20%)
    health_score = (cpu_score * 0.4) + (memory_score * 0.4) + (disk_score * 0.2)
    return round(health_score, 1)

# File upload and log analysis functions
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_log_security(log_content):
    """Analyze log content for security issues"""
    findings = {
        'failed_logins': 0,
        'suspicious_ips': [],
        'brute_force_attempts': 0,
        'unusual_patterns': [],
        'security_score': 100,
        'recommendations': []
    }

    lines = log_content.split('\n')

    # Patterns for security analysis
    failed_login_pattern = re.compile(r'Failed.*login|authentication.*failed|invalid.*password', re.IGNORECASE)
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    brute_force_pattern = re.compile(r'(multiple.*attempt|brute.*force|too.*many.*attempt)', re.IGNORECASE)

    ip_attempts = Counter()

    for line in lines:
        # Count failed logins
        if failed_login_pattern.search(line):
            findings['failed_logins'] += 1

        # Extract IPs and count attempts
        ips = ip_pattern.findall(line)
        for ip in ips:
            ip_attempts[ip] += 1

        # Check for brute force indicators
        if brute_force_pattern.search(line):
            findings['brute_force_attempts'] += 1

    # Identify suspicious IPs (high attempt counts)
    suspicious_threshold = 5
    findings['suspicious_ips'] = [ip for ip, count in ip_attempts.items() if count >= suspicious_threshold]

    # Calculate security score
    if findings['failed_logins'] > 10:
        findings['security_score'] -= 30
        findings['recommendations'].append("High number of failed logins detected")
    if findings['brute_force_attempts'] > 0:
        findings['security_score'] -= 20
        findings['recommendations'].append("Brute force attempts detected")
    if len(findings['suspicious_ips']) > 3:
        findings['security_score'] -= 25
        findings['recommendations'].append("Multiple suspicious IP addresses identified")

    findings['security_score'] = max(0, findings['security_score'])

    return findings

def get_uploaded_logs():
    """Get list of uploaded log files"""
    logs = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                stats = os.stat(filepath)
                logs.append({
                    'filename': filename,
                    'size': stats.st_size,
                    'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'path': filepath
                })
    return logs

@app.route("/api/block-ip", methods=['POST'])
def block_ip():
    data = request.get_json()
    ip = data.get('ip')
    if not ip:
        return jsonify({"success": False, "error": "IP address required"}), 400

    try:
        # In a real SOC, this would integrate with firewall/IPS systems
        # For demo purposes, we'll just log the action
        print(f"Blocking IP: {ip}")

        # Update alert action in database
        conn = sqlite3.connect("soc_alerts.db")
        cur = conn.cursor()
        cur.execute("UPDATE alerts SET action = 'BLOCK IP' WHERE ip = ?", (ip,))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": f"IP {ip} blocked successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/create-incident", methods=['POST'])
def create_incident():
    data = request.get_json()
    alert_id = data.get('alert_id')

    try:
        # Mock incident creation - in real SOC, this would create a ticket/incident
        print(f"Creating incident for alert ID: {alert_id}")
        return jsonify({"success": True, "incident_id": f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Enhanced system health endpoint
@app.route("/api/detailed-system-health")
def detailed_system_health():
    """Get detailed system health information"""
    health_data = get_detailed_system_health()
    return jsonify(health_data)

# Alert notification endpoints
@app.route("/api/send-alert", methods=['POST'])
def send_manual_alert():
    """Manually trigger alert notifications"""
    data = request.get_json()
    alert_type = data.get('type', 'manual')
    message = data.get('message', 'Manual alert triggered')

    subject = f"Manual SOC Alert - {alert_type.upper()}"
    html_message = f"""
    <h2>🚨 Manual Security Alert</h2>
    <p><strong>Type:</strong> {alert_type}</p>
    <p><strong>Message:</strong> {message}</p>
    <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """

    email_sent = send_email_alert(subject, html_message)
    notification_sent = send_system_notification("SOC Manual Alert", message)

    return jsonify({
        "success": email_sent or notification_sent,
        "email_sent": email_sent,
        "notification_sent": notification_sent
    })

# Log file management endpoints
@app.route("/api/upload-log", methods=['POST'])
def upload_log():
    """Upload log file for analysis"""
    if 'logfile' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files['logfile']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyze the uploaded log
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                analysis = analyze_log_security(content)

            return jsonify({
                "success": True,
                "filename": filename,
                "analysis": analysis,
                "message": f"Log file '{filename}' uploaded and analyzed successfully"
            })
        except Exception as e:
            return jsonify({"success": False, "error": f"Analysis failed: {str(e)}"}), 500

    return jsonify({"success": False, "error": "Invalid file type"}), 400

@app.route("/api/logs")
def get_logs():
    """Get list of uploaded log files"""
    logs = get_uploaded_logs()
    return jsonify({"logs": logs})

@app.route("/api/analyze-log/<filename>")
def analyze_log(filename):
    """Analyze a specific uploaded log file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({"success": False, "error": "Log file not found"}), 404

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            analysis = analyze_log_security(content)

        return jsonify({
            "success": True,
            "filename": filename,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Analysis failed: {str(e)}"}), 500

@app.route("/api/download-log/<filename>")
def download_log(filename):
    """Download a specific log file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({"success": False, "error": "Log file not found"}), 404

    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route("/api/delete-log/<filename>", methods=['DELETE'])
def delete_log(filename):
    """Delete a specific log file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({"success": False, "error": "Log file not found"}), 404

    try:
        os.remove(filepath)
        return jsonify({"success": True, "message": f"Log file '{filename}' deleted"})
    except Exception as e:
        return jsonify({"success": False, "error": f"Delete failed: {str(e)}"}), 500

# Enhanced alert detection with automatic notifications
@app.route("/api/check-alerts")
def check_alerts():
    """Check for new alerts and trigger notifications if needed"""
    try:
        check_login_limits()  # Check for login limit violations
        alerts = get_alerts()

        # Check for recent critical alerts (last 5 minutes)
        recent_critical = []
        five_minutes_ago = datetime.now() - timedelta(minutes=5)

        for alert in alerts:
            alert_time = datetime.strptime(alert[5], '%Y-%m-%d %H:%M:%S')
            if alert_time > five_minutes_ago and alert[3] == 'HIGH':
                recent_critical.append(alert)

        if recent_critical:
            subject = f"CRITICAL ALERTS: {len(recent_critical)} New High-Severity Threats"
            message = f"""
            <h2>🚨 Critical Security Alerts Detected</h2>
            <p><strong>Count:</strong> {len(recent_critical)}</p>
            <p><strong>Time Window:</strong> Last 5 minutes</p>
            <p><strong>Action Required:</strong> Immediate investigation needed</p>
            """

            send_email_alert(subject, message)
            send_system_notification("Critical SOC Alerts", f"{len(recent_critical)} new high-severity alerts detected!")

        return jsonify({
            "success": True,
            "alerts_checked": len(alerts),
            "critical_alerts": len(recent_critical),
            "notifications_sent": len(recent_critical) > 0
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9999)