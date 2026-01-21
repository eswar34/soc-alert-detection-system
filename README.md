# 🚨 SOCAlert Detection and Incident Analysis System

A sophisticated, cyberpunk-themed Security Operations Center (SOC) dashboard for real-time threat detection, incident response, and log analysis.

## ✨ Features

### 🎯 Core Functionality
- **Real-time Threat Detection**: Automated scanning for brute force attacks and suspicious login attempts
- **Advanced Alert Management**: Comprehensive alert filtering, sorting, and prioritization
- **Interactive Dashboard**: Modern, responsive interface with cyberpunk aesthetics
- **System Health Monitoring**: Real-time CPU, memory, disk, and network monitoring
- **Email & System Alerts**: Automatic notifications for security incidents and login limits
- **Log File Analysis**: Upload, analyze, and manage security log files
- **Export Capabilities**: Export alerts and logs in CSV or JSON format

### 🎨 Advanced UI Features
- **Cyberpunk Theme**: Matrix-style animations, terminal aesthetics, and neon color schemes
- **Sidebar Navigation**: Organized sections (Dashboard, Alerts, Analytics, Incidents, Monitoring, Log Analysis, Settings)
- **Interactive Charts**: Real-time data visualization with Chart.js
- **Alert Details Modal**: Detailed view of individual alerts with response actions
- **Drag & Drop Upload**: Easy log file uploading with progress indicators
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Keyboard Shortcuts**: Ctrl+R for refresh, Ctrl+F for search focus

### 🔧 Technical Features
- **RESTful API**: Complete API endpoints for all dashboard functions
- **SQLite Database**: Efficient local storage with timestamp-based ordering
- **Background Processing**: Asynchronous threat detection and log analysis
- **Email Integration**: SMTP-based alert notifications
- **System Notifications**: Windows toast notifications for critical alerts
- **File Upload Security**: Secure log file handling with type validation
- **Real-time Monitoring**: Live system resource tracking with health scoring
- **Error Handling**: Comprehensive error management and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone and Setup**:
```bash
cd "e:\Dot net full stack development(HCL)\js\soc-alert-detection-system"
python -m venv venv
venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
pip install flask psutil
```

3. **Configure Email (Optional)**:
Edit the email settings in `cyber_app.py`:
```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@gmail.com'
SMTP_PASSWORD = 'your-app-password'
ALERT_RECIPIENTS = ['admin@company.com']
```

4. **Initialize Database**:
```bash
python database.py
```

5. **Run the Application**:
```bash
python cyber_app.py
```

6. **Access Dashboard**:
Open http://127.0.0.1:9999 in your browser

## 📊 Dashboard Sections

### 🏠 Dashboard
- **System Health Monitor**: Real-time infrastructure metrics
- **Alert Statistics**: Severity breakdown with visual indicators
- **Threat Distribution**: Interactive pie chart of alert types
- **Activity Timeline**: Recent security events
- **Recent Activity**: Timeline of latest alerts

### 🚨 Alerts
- **Advanced Filtering**: Search by IP, user, severity, action, and time range
- **Bulk Actions**: Clear all alerts, export data
- **Alert Details**: Click any row for detailed modal view
- **Response Actions**: Block IP, investigate, create incident, escalate

### 📈 Analytics
- **Threat Intelligence**: Advanced threat analysis charts
- **Response Times**: Performance metrics visualization
- **Custom Dashboards**: Extensible analytics framework

### 📁 Incidents
- **Incident Management**: Track and manage security incidents
- **Workflow Integration**: Connect with ticketing systems
- **Escalation Matrix**: Automated incident prioritization

### 👁️ System Monitor
- **Real-time Monitoring**: Live system resource tracking
- **Performance Metrics**: CPU, memory, disk, and network stats
- **Alert Thresholds**: Configurable monitoring alerts
- **Health Score**: Overall system health assessment
- **Security Services**: Status of antivirus, EDR, DLP, SIEM

### 📄 Log Analysis
- **File Upload**: Drag & drop log file uploading
- **Security Analysis**: Automated log parsing for security issues
- **Threat Detection**: Identify failed logins, brute force attempts, suspicious IPs
- **Security Scoring**: Overall security assessment of uploaded logs
- **File Management**: View, download, and delete uploaded log files

### ⚙️ Settings
- **Alert Configuration**: Email and system notification settings
- **Threshold Settings**: Configurable alert thresholds
- **Theme Settings**: Cyberpunk theme customization
- **Manual Alerts**: Send custom security alerts

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/alerts` | GET | Get all alerts (JSON) |
| `/api/stats` | GET | Alert statistics |
| `/api/recent-activity` | GET | Recent alerts |
| `/api/system-health` | GET | Basic system monitoring data |
| `/api/detailed-system-health` | GET | Comprehensive system health data |
| `/api/alert-details/<id>` | GET | Detailed alert information |
| `/run_detector` | GET | Execute threat detection |
| `/clear_alerts` | POST | Clear all alerts |
| `/export_alerts` | GET | Export alerts (CSV/JSON) |
| `/api/block-ip` | POST | Block IP address |
| `/api/create-incident` | POST | Create security incident |
| `/api/send-alert` | POST | Send manual alert |
| `/api/upload-log` | POST | Upload log file for analysis |
| `/api/logs` | GET | Get list of uploaded logs |
| `/api/analyze-log/<filename>` | GET | Analyze specific log file |
| `/api/download-log/<filename>` | GET | Download log file |
| `/api/delete-log/<filename>` | DELETE | Delete log file |
| `/api/check-alerts` | GET | Check for new alerts and send notifications |

## 🎮 Usage Guide

### Scanning for Threats
1. Click the **SCAN** button in the header
2. The system will analyze auth.log for suspicious patterns
3. New alerts will appear in the dashboard automatically

### Managing Alerts
1. Use the **Alerts** section for detailed alert management
2. Filter by severity, IP, user, or time range
3. Click on any alert row for detailed information
4. Use action buttons to respond to threats

### System Monitoring
- View real-time system health in the **Dashboard**
- Monitor CPU, memory, and network usage in **System Monitor**
- Health score indicates overall system status
- Automatic alerts when thresholds are exceeded

### Log File Analysis
1. Navigate to **Log Analysis** section
2. Drag & drop or browse to upload log files
3. View automatic security analysis results
4. Check security score and recommendations
5. Manage uploaded files (view, download, delete)

### Email & System Alerts
- **Automatic**: Alerts sent when login limits are exceeded
- **Manual**: Use "Send Alert" button in System Monitor
- **Configuration**: Set up email settings in the code
- **System Notifications**: Windows toast notifications for critical alerts

### Exporting Data
1. Navigate to the **Alerts** section
2. Click **Export** button
3. Choose CSV or JSON format
4. File will download automatically

## 🔒 Security Features

- **Input Validation**: All user inputs are validated
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Sanitized output rendering
- **CSRF Protection**: Token-based request validation
- **File Upload Security**: Type validation and secure filename handling
- **Secure Headers**: Flask security headers enabled
- **Log Analysis**: Automated detection of security patterns
- **Alert Notifications**: Real-time security incident alerting

## 📱 Responsive Design

The dashboard is fully responsive and works on:
- **Desktop**: Full feature set with sidebar navigation
- **Tablet**: Collapsible sidebar, optimized layouts
- **Mobile**: Single-column layout, touch-friendly controls

## 🛠️ Development

### Project Structure
```
soc-alert-detection-system/
├── cyber_app.py              # Main Flask application
├── database.py               # Database initialization
├── detector.py               # Threat detection logic
├── templates/
│   └── cyber_alerts.html     # Main dashboard template
├── uploads/                  # Uploaded log files directory
├── logs/                     # System logs directory
└── README.md                # This file
```

### Adding New Detection Rules
1. Modify `detector.py` to add new patterns
2. Update the database schema if needed
3. Test with sample log data

### Extending the API
1. Add new routes in `cyber_app.py`
2. Implement proper error handling
3. Update API documentation

### Customizing Alerts
1. Edit email configuration in `cyber_app.py`
2. Modify alert thresholds in the settings
3. Customize notification messages

## 🚨 Alert System

### Automatic Alerts
- **Login Limit Alerts**: Triggered when failed login attempts exceed threshold
- **System Health Alerts**: Notifications for resource usage spikes
- **Security Incident Alerts**: Real-time notifications for detected threats

### Manual Alerts
- Send custom alerts via the dashboard
- Choose alert type and message
- Immediate email and system notifications

### Alert Channels
- **Email**: SMTP-based notifications to configured recipients
- **System**: Windows toast notifications
- **Dashboard**: Real-time visual indicators

## 📊 Log Analysis Features

### Supported File Types
- `.log` - System log files
- `.txt` - Text log files
- `.csv` - Comma-separated log data
- `.json` - JSON formatted logs

### Security Analysis
- **Failed Login Detection**: Identifies authentication failures
- **Brute Force Detection**: Recognizes repeated failed attempts
- **Suspicious IP Analysis**: Flags IPs with high failure rates
- **Security Scoring**: Overall security assessment (0-100)

### Analysis Results
- Detailed security findings
- Actionable recommendations
- Visual security score indicator
- Downloadable analysis reports

## 🚨 Troubleshooting

### Common Issues

**App won't start**:
- Check Python version (3.8+ required)
- Ensure all dependencies are installed
- Verify database file exists

**No alerts detected**:
- Check that auth.log exists and is readable
- Verify detector.py has proper permissions
- Check log file format matches expected patterns

**Email alerts not working**:
- Verify SMTP settings in `cyber_app.py`
- Check email credentials and app passwords
- Ensure SMTP server allows connections

**Log upload fails**:
- Check file size limits
- Verify supported file types
- Ensure uploads directory has write permissions

**System monitoring unavailable**:
- Install psutil: `pip install psutil`
- Check system permissions for resource monitoring
- Some metrics may not be available on all systems

### Debug Mode
Run with debug enabled for detailed error messages:
```bash
python cyber_app.py
```

## 📈 Performance

- **Database**: SQLite with optimized queries
- **Frontend**: Vanilla JavaScript with minimal dependencies
- **Charts**: Lightweight Chart.js library
- **Real-time**: Polling-based updates (WebSocket ready)
- **File Processing**: Efficient log analysis with streaming

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue with detailed information

---

**Version**: 2.2.0
**Last Updated**: January 2026
**Author**: SOC Development Team
