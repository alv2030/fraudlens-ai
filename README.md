# FraudLens AI v2 Final — Real-Time Fraud Detection & Investigation Platform

FraudLens AI v2 is a GitHub-ready ML engineering portfolio project for detecting suspicious financial transactions in near real time. It combines model training, hybrid fraud scoring, Kafka/Spark streaming design, PostgreSQL alert workflow, MLflow/local registry metadata, SHAP-style explainability, FastAPI services, Streamlit dashboard, Docker Compose, and tests.

## Why this version is stronger

This v2 final build fixes the main gaps from the earlier versions:

- Full project package, not a patch-only update
- API auto-seeds a demo model if no trained model exists
- PostgreSQL schema initializes automatically when infrastructure is available
- Alert workflow persists transactions, predictions, alerts, and status history
- Spark Structured Streaming job includes a PostgreSQL micro-batch sink path
- MLflow registry wrapper has local JSON fallback so the repo works without MLflow server
- Docker Compose includes API, dashboard, MLflow, Kafka, Redis, PostgreSQL, and streaming service
- Dashboard no longer hard-fails when model is missing
- Tests cover API, rules, feature engineering, validation, prediction bootstrap, and streaming batch scoring

## Architecture

```text
Historical Fraud Dataset / Demo Generator
        ↓
Data Validation + Feature Engineering
        ↓
Model Training + Threshold Strategy
        ↓
MLflow Tracking + Local Model Registry
        ↓
Production Model Artifact

Transaction Simulator / Kafka Producer
        ↓
Kafka Topic: transactions
        ↓
Spark Structured Streaming Micro-Batches
        ↓
ML Model + Rule Engine
        ↓
SHAP-style Explanation
        ↓
PostgreSQL: Transactions, Predictions, Alerts, Status History
        ↓
FastAPI + Streamlit Investigator Dashboard
```

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| ML | Scikit-Learn, XGBoost, SHAP, MLflow |
| Streaming | Kafka, Spark Structured Streaming |
| Storage | PostgreSQL, Redis |
| API | FastAPI, Pydantic |
| Dashboard | Streamlit, Plotly |
| DevOps | Docker, Docker Compose, Pytest, GitHub Actions |

## Project Structure

```text
fraudlens-ai-v2-final/
├── Dockerfile.api
├── Dockerfile.dashboard
├── Dockerfile.streaming
├── docker-compose.yml
├── Makefile
├── README.md
├── requirements.txt
├── src/
│   ├── api/          # FastAPI scoring, admin bootstrap, alert workflow APIs
│   ├── dashboard/    # Streamlit investigator dashboard
│   ├── data/         # data generation/loading, validation, PostgreSQL persistence
│   ├── features/     # behavioral features and feature-store interface
│   ├── models/       # training, seed model, prediction, SHAP explanation, registry
│   ├── rules/        # fraud rule engine
│   ├── simulator/    # transaction generator
│   └── streaming/    # Kafka producer/consumer and Spark streaming sink
├── sql/              # PostgreSQL schema and analytics queries
├── tests/            # pytest coverage
├── reports/          # system design and model documentation
└── artifacts/        # model artifacts and registry metadata
```

## Local Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make seed-model
make api
```

Open API docs:

```text
http://localhost:8000/docs
```

Run dashboard:

```bash
make dashboard
```

## Docker Quickstart

```bash
docker compose up --build
```

Useful URLs:

```text
API:       http://localhost:8000/docs
Dashboard: http://localhost:8501
MLflow:    http://localhost:5000
```

## API Examples

Score and persist a transaction:

```bash
curl -X POST "http://localhost:8000/score-transaction?persist=true" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id":"txn_demo_001",
    "customer_id":"10001",
    "amount":1250.00,
    "transaction_hour":2,
    "is_foreign_transaction":1,
    "is_new_device":1,
    "is_card_not_present":1,
    "velocity_1h":6,
    "merchant_risk_score":2,
    "customer_avg_amount_30d":85.00,
    "merchant_category":"electronics",
    "merchant_country":"BR",
    "device_type":"mobile"
  }'
```

List alerts:

```bash
curl http://localhost:8000/alerts
```

Update alert status:

```bash
curl -X PATCH http://localhost:8000/alerts/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"UNDER_REVIEW","changed_by":"analyst","notes":"Reviewing customer history."}'
```

## Fraud Scoring

```text
Final Risk Score = 70% ML Fraud Probability + 30% Rule Score
```

Rule signals include high amount deviation, foreign country, new device, card-not-present, high-risk merchant, high transaction velocity, and late-night activity.

## Model Strategy

Included:

- Logistic Regression baseline
- Random Forest baseline
- XGBoost production candidate
- Demo seed Random Forest fallback for zero-friction app startup
- MLflow experiment tracking with local registry fallback
- PR-AUC, recall, precision, F1, ROC-AUC, and threshold tracking

Recommended real dataset: Kaggle Credit Card Fraud Detection Dataset. Place it at:

```text
data/raw/creditcard.csv
```

The repo also works without external data by generating a demo dataset.

## Alert Workflow

```text
OPEN → UNDER_REVIEW → CONFIRMED_FRAUD / FALSE_POSITIVE → CLOSED
```

Every status update is stored in `alert_status_history`.

## Testing

```bash
pytest -q
```

## Resume Bullets

```text
FraudLens AI v2 — Real-Time Fraud Detection Platform | Python, Kafka, Spark, XGBoost, MLflow, PostgreSQL, Redis, SHAP, FastAPI, Streamlit, Docker

• Built an end-to-end real-time fraud detection platform with Kafka ingestion, Spark Structured Streaming micro-batch scoring, PostgreSQL alert persistence, FastAPI services, and Streamlit investigation dashboards.
• Trained and optimized fraud detection models for highly imbalanced transaction data using XGBoost, cost-sensitive learning, threshold tuning, and PR-AUC/recall-focused evaluation.
• Designed a hybrid scoring engine combining ML probability, behavioral velocity rules, customer risk features, and SHAP-style explainability for investigator review.
• Implemented MLflow experiment tracking, local model registry fallback, Dockerized services, PostgreSQL workflow tables, and automated tests for production-style ML delivery.
```

## Scope Note

This is a portfolio-grade local system, not a PCI-compliant banking production system. Real production use requires stronger security, identity/access controls, audit logging, PII governance, drift monitoring, model risk management, and compliance review.


## Dashboard Demo



The Streamlit dashboard provides a local fraud monitoring workflow with generated transactions, risk scoring, rule-based explanations, and trend visualization.



![FraudLens Dashboard](docs/screenshots/Dashboard.png)



![Risk Score Trend](docs/screenshots/Risk%20Score%20Trend.png)

## System Architecture

![FraudLens Architecture](docs/architecture.png)
