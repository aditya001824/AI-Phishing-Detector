# 🛡️ AI Phishing Detector

An intelligent Machine Learning-based Phishing Email and SMS Detection system. Built with Python, Scikit-Learn, and Flask, this application analyzes text messages and URLs to identify potential phishing attacks with high confidence.

---

## 🚀 Features

- **Machine Learning Powered**: Trained using TF-IDF vectorization and Logistic Regression for fast, accurate classification.
- **Dual Interface**:
  - 🌐 **Interactive Web UI**: Modern, responsive dashboard to test emails and messages in real-time.
  - 💻 **Command-Line Interface (CLI)**: Quick terminal-based scanning tool for developers and sysadmins.
- **RESTful API**: Easily integrate phishing detection endpoints into existing email gateways or security pipelines.
- **Confidence Scoring**: Returns risk classifications and prediction confidence.
- **Automated CI/CD**: Automated testing workflows and daily repository health maintenance.

---

## 📂 Project Architecture

```
AI-Phishing-Detector/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # Automated test runner
│       └── daily-commit.yml       # Scheduled maintenance workflow
├── dataset/
│   └── phishing_email.csv         # Labeled training dataset
├── static/
│   ├── script.js                  # Frontend async API interactions
│   └── style.css                  # UI styling and theme
├── templates/
│   └── index.html                 # Web dashboard interface
├── tests/
│   ├── test_app.py                # Web server endpoint test suite
│   └── test_detector.py           # Core detector logic test suite
├── app.py                         # Flask web server & API
├── detector.py                    # Modular CLI detection tool
├── train_model.py                 # Training script with performance metrics
├── requirements.txt               # Project dependencies
├── phishing_model.pkl             # Serialized Logistic Regression model
└── vectorizer.pkl                 # Serialized TF-IDF vectorizer
```

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/aditya001824/AI-Phishing-Detector.git
cd AI-Phishing-Detector
```

### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📖 Usage

### Running the Web Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

### Using the CLI Detector
Run the interactive CLI tool:
```bash
python detector.py
```
Or scan directly from command arguments:
```bash
python detector.py --text "URGENT: Your account has been suspended! Click here to verify."
```

### Training or Retraining the Model
To re-train the model with updated data in `dataset/`:
```bash
python train_model.py
```

---

## 📡 API Reference

### Predict Message
**Endpoint**: `POST /predict`  
**Content-Type**: `application/json`

#### Request Body
```json
{
  "message": "Dear customer, claim your \$1000 gift card immediately by visiting http://bit.ly/scam"
}
```

#### Response
```json
{
  "result": "phishing",
  "confidence": 0.98
}
```

---

## 🧪 Testing

Run the test suite with `pytest`:
```bash
pytest
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.