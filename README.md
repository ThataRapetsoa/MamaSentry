# MamaSentry — Digital Fraud Shield 🛡️🇿🇦

> "Before you click. Before you pay. Ask MamaSentry."

Digital financial fraud and social engineering scams are devastating South African communities, particularly targeting women, small business operators, and the elderly. Cybercriminals aggressively exploit communication channels like WhatsApp and SMS through sophisticated phishing links, fake digital payment notifications, and administrative impersonation tactics. Traditional cybersecurity solutions are built for large corporate environments, leaving everyday mobile users completely exposed to losing their life savings to digital fraud.

**MamaSentry** is a lightweight, localized mobile security gatekeeper designed to intercept, analyze, and neutralize incoming social engineering threats before users fall victim to them. The system ingests message metadata, text snippets, or suspicious URLs, parsing the content for known fraud signals using deterministic pattern-matching combined with lightweight AI classification.

---

## ✨ Key Features (MVP)
* **Multi-Input Ingestion:** Accepts pasted WhatsApp/SMS text strings or suspicious URLs for immediate evaluation.
* **Deterministic Threat Detection:** Uses regex-based URL validation guardrails and South African specific threat-intelligence pattern matching.
* **Transparent Risk Engine:** Employs a clear, points-based scoring matrix to avoid "black box" machine learning confusion.
* **Human-Centric Explanations:** Translates underlying technical flags into simple, readable explanations and clear actionable next steps.

---

## 🏗️ Architecture & Core Flow
MamaSentry follows a clean, modular pipeline: **Detect ➔ Explain ➔ Protect**.

1. **Frontend / UI:** Simple web interface for users to submit messages or URLs and view clean results.
2. **API Backend:** A FastAPI routing engine that receives payloads and manages parallel security service tasks.
3. **Input Processor:** Sanitizes and normalizes raw text before evaluating indicators.
4. **Threat Detection & Risk Engine:** Scans text against regex collections and rulesets, computing a cumulative priority score.

---

## 📊 Risk Scoring Matrix & Thresholds

The underlying analysis engine processes inputs using prototype threat indicator values:

| Threat Signal Found | Weight |
| :--- | :---: |
| URL / Domain Mismatch (e.g., lookalike bank links) | +30 |
| Credential / OTP Request | +25 |
| Suspicious / Unverified URL | +25 |
| Financial Pressure / Money Requests | +20 |
| Impersonation Tactics | +20 |
| Fake Payment / EFT Notifications | +20 |
| Urgent / Scare Language | +15 |

### 🚨 Output States
* 🟢 **SAFE** (0 – 24 Points): Standard conversation text; no suspicious actions found.
* 🟡 **SUSPICIOUS** (25 – 59 Points): Flagged for user caution. Mismatches or unknown requests identified.
* 🔴 **CRITICAL THREAT** (60+ Points): Direct match with high-level banking fraud, fake payment notifications, or phishing templates. Immediate risk mitigation recommended.

---

## 📂 Project Structure

```text
mamasentry/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── main.py                     # Application entry point
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API Endpoints for message analysis
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response validation schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analyzer.py         # Main analysis pipeline orchestrator
│   │   ├── risk_engine.py      # Computes prototype scores and threat tiering
│   │   ├── url_checker.py      # Structure and domain validation service
│   │   └── ai_classifier.py    # Optional contextual classification block
│   ├── rules/
│   │   ├── __init__.py
│   │   └── fraud_patterns.json # Configurable South African scam terms & patterns
│   └── utils/
│       ├── __init__.py
│       └── text_cleaner.py     # Strips and sanitizes message payloads
├── tests/
│   ├── test_analyzer.py
│   ├── test_risk_engine.py
│   └── test_url_checker.py
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── main.js
│   │   ├── api.js              # Fetch layer binding to backend API routes
│   │   └── components/
│   │       ├── InputForm.js
│   │       ├── RiskResult.js   # Dynamic presentation component (Safe/Suspicious/Threat)
│   │       └── ThreatReasons.js
│   └── styles.css
└── sample_data/
    ├── safe_messages.json
    ├── suspicious_messages.json
    └── critical_messages.json
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Node.js (Optional, if extending the frontend package management layout)

### 🛠️ Backend Setup
1. Clone the project repository and move into the working root directory:
   ```bash
   cd mamasentry
   ```
2. Create and activate your virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install required application dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template and spin up the microservice application server:
   ```bash
   cp .env.example .env
   python main.py
   ```
   *The api server will run on `http://127.0.0.1:8000` by default.*

### 💻 Frontend Setup
1. Open a terminal tab and transition into the UI directory:
   ```bash
   cd frontend
   ```
2. Serve the presentation files using a local development server extension or run:
   ```bash
   python -m http.server 3000
   ```
3. Open your favorite web browser and point it directly to `http://localhost:3000`.

---

## 🎯 South African Context Focus
MamaSentry targets hyper-local variants of digital fraud widely seen across networks like MTN, Vodacom, and Telkom:
* **Fake Bank Alerts:** Impersonations of Capitec, FNB, Standard Bank, or Absa claiming account blocks.
* **Fake EFT/Payment Confirmations:** Fabricated proof of payment templates targeting digital sellers.
* **The "Hi Mom / Hi Dad" WhatsApp Scam:** Emergency family profile impersonations asking for rapid e-wallet transfers.
* **Customs/SARS Exploitations:** South African Post Office tracking links demanding immediate balance payments.
