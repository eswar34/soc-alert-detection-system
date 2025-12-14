# SOC Alert Detection & Automated Incident Response System

## 📌 Project Overview
This project simulates a **Security Operations Center (SOC)** alert detection and response system.  
It analyzes system authentication logs to detect suspicious activities such as brute-force login attempts, classifies alerts based on severity, triggers automated response actions, and displays alerts on a web-based dashboard.

The system is designed to reflect **real-world SOC workflows** used in enterprise security environments.

---

## 🎯 Purpose
- Detect brute-force and suspicious login attempts
- Reduce noise by filtering normal behavior
- Classify security incidents by severity
- Simulate automated incident response
- Assist SOC analysts with visibility and reporting

---

## 🛠️ Technologies Used
- **Python**
- **Bash**
- **SQLite**
- **Flask**
- **HTML & CSS**
- **Git & GitHub**

---

## 🧱 Project Architecture
System Authentication Logs
↓
Detection Engine (Python)
↓
Alert Database (SQLite)
↓
Automated Response (Bash)
↓
SOC Dashboard (Flask Web UI)
↓
Incident Report Generation

yaml
Copy code

---

## 📂 Project Structure
soc_alert_system/
│── app.py
│── database.py
│── detector.py
│── responder.sh
│── report.py
│── templates/
│ └── alerts.html
│── logs/
│ └── auth.log
│── README.md
│── .gitignore

yaml
Copy code

---

## ⚙️ How It Works
1. Authentication logs are analyzed for failed login patterns
2. Detection rules identify brute-force attempts
3. Alerts are classified into severity levels
4. Automated response actions are triggered (simulated)
5. Alerts are visualized on a SOC dashboard
6. Incident reports are generated for documentation

---

## 🚨 Detection Rules Implemented
- Multiple failed login attempts from same IP
- Threshold-based severity classification
- Noise reduction by ignoring successful logins

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.x
- Flask

### Steps
```bash
pip install flask
python database.py
python detector.py
python app.py
Open browser:

cpp
Copy code
http://127.0.0.1:5000
📄 Incident Report
Generate report using:

bash
Copy code
python report.py
This creates incident_report.txt summarizing detected incidents.

🔐 Security Considerations
Read-only log analysis

No destructive system commands

Automated responses are safely simulated

Designed for Linux SOC environments

🎓 Learning Outcomes
SOC alert detection logic

Log analysis and correlation

Automated incident response concepts

Security-focused web dashboards

Incident reporting and documentation

👨‍🎓 Author
Eswar Kumar
Cybersecurity / SOC Analyst Aspirant

⚠️ Disclaimer
This project is for educational purposes only and uses simulated data.
No real systems or production environments are affected.

yaml
Copy code
