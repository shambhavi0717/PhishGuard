# PhishGuard – AI-Based Ethical Phishing Simulation & Awareness Platform

PhishGuard is a web-based cybersecurity awareness platform designed to simulate phishing campaigns in a safe, controlled environment. It helps demonstrate how phishing simulations can be created, monitored, analyzed, and used for security awareness training.

The platform also includes a lightweight AI-based email classifier that analyzes email text and predicts whether it is likely to be **phishing** or **legitimate**.

> **Safety Notice:** PhishGuard is designed for educational and cybersecurity awareness purposes. It uses simulated campaign activity and does not collect real user credentials or conduct real-world phishing campaigns.

---

## 📌 Project Overview

Phishing is one of the most common forms of social engineering used to deceive users into interacting with malicious messages.

PhishGuard provides a local web application where simulated phishing awareness campaigns can be created and analyzed. The application combines:

- Phishing campaign management
- Simulated campaign activity
- Campaign performance metrics
- Security awareness training
- AI-based phishing email detection
- Dashboard-based analytics

The project demonstrates how these components can work together as a basic cybersecurity awareness platform.

---

## 🎯 Objectives

The main objectives of PhishGuard are to:

- Simulate phishing awareness campaigns in a controlled environment.
- Provide customizable phishing campaign templates.
- Store campaign information and metrics using SQLite.
- Simulate participant activity such as email delivery, opening, clicking, and reporting.
- Display campaign performance through dashboard statistics and charts.
- Provide security awareness guidance for identifying phishing indicators.
- Use a machine-learning model to classify email messages as phishing or legitimate.

---

## ✨ Features

### 1. Phishing Simulation Management

Users can create simulated phishing awareness campaigns by providing:

- Campaign name
- Target group
- Campaign description
- Email template
- Start date
- Campaign duration

Available simulation templates include:

- Password Reset
- Payment Verification
- Security Alert

Campaign information is stored in the SQLite database.

---

### 2. Campaign Details & Metrics

Each campaign has a dedicated details page displaying:

- Participants
- Emails delivered
- Emails opened
- Links clicked
- Reported emails
- Awareness score

Campaign activity can be simulated locally using the **Simulate Campaign Activity** function.

The simulation generates controlled activity data for demonstration purposes.

---

### 3. Security Dashboard

The dashboard provides an overview of the current campaign data.

It displays:

- Total simulations
- Total participants
- Phishing click rate
- Security/awareness score
- Simulation performance
- Risk distribution
- Recent simulations

The charts are connected to the application's database so that campaign activity is reflected in the dashboard.

---

### 4. AI-Based Phishing Email Analyzer

PhishGuard includes a lightweight machine-learning based email classifier.

The analyzer uses:

- TF-IDF text vectorization
- Logistic Regression classification

Users can paste an email message into the AI Threat Analyzer.

The model predicts whether the message is:

- `phishing`
- `legitimate`

The model was trained using a small educational dataset containing example phishing and legitimate email messages.

---

### 5. Security Awareness Training

The Awareness Training section provides guidance on common phishing indicators, including:

- Urgent or threatening language
- Suspicious links
- Unusual sender addresses
- Requests for sensitive information
- Generic greetings
- Unexpected requests

The page also provides general guidance to verify suspicious messages before taking action.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application and AI development |
| Flask | Web application framework |
| SQLite | Local database |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Interactive dashboard components |
| Chart.js | Dashboard charts |
| Pandas | Dataset handling |
| Scikit-learn | Machine learning |
| TF-IDF | Email text feature extraction |
| Logistic Regression | Phishing email classification |

---

## 🧠 Machine Learning Workflow

The AI phishing detector follows this basic workflow:

```text
Email Text
    ↓
Text Preprocessing
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression Model
    ↓
Prediction
    ↓
Phishing / Legitimate

## 🔄 Application Workflow

                    ┌───────────────────┐
                    │    PhishGuard     │
                    │   Web Dashboard   │
                    └─────────┬─────────┘
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
      Create Simulation   AI Analyzer   Awareness Training
             │                │                │
             ↓                ↓                ↓
        SQLite DB       ML Prediction     Security Tips
             │
             ↓
     Simulate Campaign
             │
             ↓
      Campaign Metrics
             │
             ↓
     Dashboard Analytics