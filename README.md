# 🛡️ STARLIGHT AI – Enterprise Cybersecurity Recommendation System

STARLIGHT AI is an AI-powered Enterprise Cybersecurity Recommendation System that helps organizations identify their cybersecurity risk level and recommends the most suitable cybersecurity solutions using Machine Learning and rule-based risk analysis.

The application allows organizations to assess their current security posture by providing information about their infrastructure, security controls, compliance requirements, and threat concerns. Based on this information, the system predicts the best cybersecurity solution and provides enterprise-grade recommendations.

---

# 🚀 Features

- 🔐 User Authentication (Register/Login)
- 👤 Role-Based User Management
- 🤖 Machine Learning Based Recommendation Engine
- 📊 Enterprise Risk Assessment
- 📈 Risk Score Calculation
- 🎯 Top Security Solution Recommendation
- 📋 Multiple Security Recommendations
- 🛡️ Product Recommendation Database
- 📚 Assessment History
- 📡 REST APIs
- 🗄️ MySQL Database Integration
- 🌐 Responsive Web Interface
- 📄 JSON API Responses

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
          Flask Web Application
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
Machine Learning      Rule-Based Engine
 Recommendation        Risk Calculation
        │                    │
        └─────────┬──────────┘
                  ▼
      Cybersecurity Recommendations
                  │
                  ▼
           MySQL Database
```

---

# 🛠️ Tech Stack

## Backend

- Python 3.x
- Flask
- Scikit-Learn
- NumPy
- Pandas
- Joblib

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

## Database

- MySQL

## Machine Learning

- Scikit-Learn
- Label Encoder
- Classification Model

---

# 📂 Project Structure

```
STARLIGHT/
│
├── app.py
├── recommendation_model.pkl
├── label_encoder.pkl
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── history.html
│   └── forgot_password.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── dataset/
│
├── screenshots/
│
└── README.md
```

---

# 🔍 Machine Learning Pipeline

The recommendation engine follows these steps:

1. Collect enterprise security information
2. Validate user input
3. Preprocess data
4. Calculate enterprise risk score
5. Predict recommended cybersecurity solution
6. Calculate prediction confidence
7. Generate top recommendations
8. Store assessment history
9. Display results

---

# 📊 Input Parameters

The model uses the following enterprise security parameters:

| Feature | Description |
|----------|-------------|
| Industry | Business Sector |
| Employees | Organization Size |
| Cloud Usage | Cloud Adoption Level |
| Firewall Installed | Yes / No |
| EDR Installed | Yes / No |
| SIEM Installed | Yes / No |
| Compliance Requirement | ISO27001, PCI-DSS, HIPAA, etc. |
| Main Threat Concern | Primary Security Concern |
| Security Budget | Organization Budget |

---

# 🛡️ Risk Assessment

The rule engine evaluates:

- Firewall Availability
- Endpoint Detection & Response
- SIEM Deployment
- Cloud Adoption
- Company Size
- Security Budget
- Industry Risk
- Compliance Standards
- Threat Landscape

Risk Levels:

- 🟢 Low
- 🟡 Medium
- 🟠 High
- 🔴 Critical

---

# 🤖 Supported Cybersecurity Solutions

The recommendation engine supports multiple enterprise cybersecurity solutions, including:

- SIEM
- EDR
- XDR
- IAM
- PAM
- CASB
- Cloud Security Platform
- MDR
- SOC-as-a-Service
- WAF
- DLP
- Email Security Gateway
- Vulnerability Management
- Threat Intelligence Platform
- ZTNA
- Ransomware Protection
- Data Encryption Platform

---

# 💾 Database

The application stores:

- User Information
- Authentication Data
- Assessment History
- Risk Scores
- Recommended Solutions
- Confidence Scores

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/starlight-ai.git

cd starlight-ai
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure MySQL

Create a database:

```sql
CREATE DATABASE starlight_ai;
```

Update the MySQL configuration in **app.py**:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "starlight_ai"
}
```

---

## Run Application

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home |
| POST | /register | Register User |
| POST | /login | Login |
| GET | /logout | Logout |
| POST | /predict | Generate Recommendation |
| GET | /history | Assessment History |
| GET | /health | Health Check |
| GET | /model-status | Model Status |

---

# 📈 Example Workflow

1. Register an account
2. Login
3. Fill enterprise assessment form
4. Submit assessment
5. AI predicts best cybersecurity solution
6. View risk score
7. View confidence score
8. Review recommended products
9. Save assessment history

---

# 📷 Screenshots

Add screenshots here.

```
screenshots/

Home Page
Login
Dashboard
Prediction Result
History
```

---

# 🎯 Future Enhancements

- Email OTP Verification
- Password Reset
- Admin Dashboard
- Vendor Comparison
- PDF Report Generation
- Explainable AI
- Cloud Deployment
- Docker Support
- Kubernetes Deployment
- Multi-language Support
- Advanced Analytics Dashboard

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Parth Verma**

- GitHub: https://github.com/parthverma9805
- LinkedIn: https://www.linkedin.com/in/parth-verma-8a4126295/

---

## ⭐ If you found this project useful, don't forget to star the repository!
