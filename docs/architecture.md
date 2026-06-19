# Architecture

FraudLens AI is organized around three workflows:

1. Online scoring: FastAPI receives a transaction, validates schema, calculates ML probability and rule score, returns decision/reason codes.
2. Analyst review: Streamlit dashboard submits transactions and displays scores/explanations.
3. Batch training: CSV transaction data is validated, transformed into features, trained, evaluated, and persisted as a model artifact.

## Design choices

- FastAPI for typed API contracts and OpenAPI documentation.
- PostgreSQL for transactional persistence and audit-style history tables.
- MLflow-compatible metrics output for experiment tracking.
- Docker Compose for reproducible local review by hiring managers.
- Pytest for unit and API contract validation.

## Limitations

- Demo data is synthetic.
- No real PCI controls.
- No real bank transaction data.
- Cloud deployment templates are examples until deployed.
