# 🛡️ PhishGuard AI - Phishing Detection System

[![CI Build](https://github.com/aditya001824/AI-Phishing-Detector/actions/workflows/ci.yml/badge.svg)](https://github.com/aditya001824/AI-Phishing-Detector/actions/workflows/ci.yml)
[![Daily Maintenance](https://github.com/aditya001824/AI-Phishing-Detector/actions/workflows/daily-commit.yml/badge.svg)](https://github.com/aditya001824/AI-Phishing-Detector/actions/workflows/daily-commit.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker Support](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](Dockerfile)

An intelligent, hybrid Machine Learning and Heuristic Security system designed to detect and explain phishing emails, SMS spam, and malicious links in real-time. Built with Python, Scikit-Learn, and Flask.

---

## 🚀 Key Features

- **🧠 Machine Learning Core**: 2-gram TF-IDF vectorizer paired with a high-performance Logistic Regression classifier (**97.76% accuracy**).
- **🔍 Heuristic Risk Engine**:
  - IP-based URL detection (e.g. `http://192.168.x.x/login`)
  - Shortened URL expander & detection (e.g. `bit.ly`, `tinyurl.com`)
  - Abused TLD scanner (`.xyz`, `.top`, `.loan`, `.tk`, etc.)
  - High-urgency and financial extortion/prize keyword extraction
- **🌐 Interactive Web Dashboard**: Modern glassmorphism UI featuring:
  - Visual confidence meter
  - Granular risk level indicators (`LOW`, `MEDIUM`, `HIGH`)
  - Real-time threat indicator breakdown
  - 1-click test sample presets
- **💻 CLI Scanner**: Direct terminal utility with argument flags (`-t / --text`, `-f / --file`).
- **⚡ Ultra-Low Latency**: ~**0.4 ms** average latency per prediction (~**2,300+ requests/sec**).
- **🐳 Container Ready**: Multi-stage `Dockerfile` and `docker-compose.yml` included.
- **🔄 CI/CD & Automation**: Continuous integration testing and daily maintenance automation.

---

## 📂 Project Architecture

```
AI-Phishing-Detector/
├── .github/
│   ├── ISSUE_TEMPLATE/            # Bug report and feature request templates
│   ├── pull_request_template.md   # Pull request checklist
│   └── workflows/
│       ├── ci.yml                 # Automated test runner on push & PR
│       └── daily-commit.yml       # Scheduled maintenance workflow
├── dataset/
│   └── phishing_email.csv         # Labeled training dataset (5,500+ records)
├── static/
│   ├── script.js                  # Frontend async API interactions & UI logic
│   └── style.css                  # Modern glassmorphism styling
├── templates/
│   └── index.html                 # Responsive web dashboard
├── tests/
│   ├── __init__.py
│   ├── test_app.py                # Web server endpoint test suite
│   ├── test_detector.py           # Core detector logic test suite
│   └── test_heuristics.py         # Heuristic rule engine test suite
├── app.py                         # Flask web server & REST API
├── detector.py                    # Modular CLI detection tool & hybrid engine
├── heuristics.py                  # URL parser and heuristic risk analyzer
├── train_model.py                 # Training script with performance metrics
├── benchmark.py                   # Latency & throughput benchmark utility
├── Dockerfile                     # Container deployment image
├── docker-compose.yml             # Single-command container runner
├── requirements.txt               # Project dependencies
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── SECURITY.md                    # Security policy and vulnerability disclosure
├── phishing_model.pkl             # Serialized Logistic Regression model
└── vectorizer.pkl                 # Serialized TF-IDF vectorizer
```

---

## 🛠️ Quick Start

### 1. Local Setup

```bash
# Clone repository
git clone https://github.com/aditya001824/AI-Phishing-Detector.git
cd AI-Phishing-Detector

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run with Docker 🐳

```bash
# Using docker-compose
docker-compose up --build

# Or standard docker build
docker build -t phishguard .
docker run -p 5000:5000 phishguard
```

Open `http://127.0.0.1:5000` in your browser.

---

## 📖 Usage & Examples

### Web Dashboard
```bash
python app.py
```

### CLI Analysis
```bash
# Interactive mode
python detector.py

# Direct text analysis
python detector.py --text "URGENT: Your account suspended! Verify at http://192.168.1.1/login"

# File analysis
python detector.py --file email_sample.txt
```

### Run Benchmarks
```bash
python benchmark.py
```

---

## 📡 REST API Reference

### 1. Health Check
* **Method**: `GET /health`
* **Response**:
```json
{
  "model_loaded": true,
  "status": "healthy"
}
```

### 2. Predict Message
* **Method**: `POST /predict`
* **Headers**: `Content-Type: application/json`
* **Payload**:
```json
{
  "message": "URGENT: Your account has been suspended! Verify your login immediately at http://192.168.1.1/reset"
}
```
* **Response**:
```json
{
  "result": "phishing",
  "is_phishing": true,
  "confidence": 0.985,
  "risk_level": "HIGH",
  "heuristic_score": 75,
  "flags": [
    "Contains direct IP address URL (high phishing risk)",
    "High-urgency language detected: 'urgent, account suspended, verify your account'"
  ],
  "url_analysis": {
    "url_count": 1,
    "has_ip_address_url": true,
    "has_shortened_url": false,
    "suspicious_tlds": []
  }
}
```

---

## 🧪 Testing

Run all unit and integration test suites:
```bash
python -m unittest discover -s tests
```

---

## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.