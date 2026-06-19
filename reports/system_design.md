# System Design — FraudLens AI Pro

FraudLens AI Pro is designed as a portfolio-grade ML engineering system. The main goal is to demonstrate the full lifecycle of a real-time fraud detection platform: data ingestion, feature engineering, model training, model registry, streaming inference, explainability, persistence, and alert investigation.

## Core production patterns demonstrated

1. Event-driven ingestion through Kafka.
2. Streaming processing through Spark Structured Streaming job wiring.
3. Hybrid fraud decisioning using ML probability and deterministic fraud rules.
4. PostgreSQL-backed alert workflow and alert status history.
5. SHAP explanation layer for model transparency.
6. MLflow-compatible model tracking and registry metadata.
7. Dockerized API and dashboard services.

## Main scoring flow

```text
Incoming transaction
→ feature enrichment
→ ML probability
→ rule score
→ final risk score
→ SHAP explanation
→ prediction persistence
→ alert creation when threshold is exceeded
```

## Alert lifecycle

```text
OPEN
→ UNDER_REVIEW
→ CONFIRMED_FRAUD or FALSE_POSITIVE
→ CLOSED
```

This makes the project more realistic than a single model notebook because it includes the operational workflow investigators would use after a model flags a transaction.
