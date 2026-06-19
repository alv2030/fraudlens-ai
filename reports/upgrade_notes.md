# Upgrade Notes

This Pro version upgrades the original project in the following areas:

- Replaced Spark placeholder with a real Spark Structured Streaming job skeleton that reads Kafka JSON, parses a schema, applies a scoring UDF, and writes a scored stream.
- Added PostgreSQL-backed alert workflow functions for listing alerts and updating alert status.
- Added FastAPI endpoints for `/alerts` and `/alerts/{alert_id}/status`.
- Added SHAP explanation support with a rule-based fallback for runtime reliability.
- Added MLflow model registration wrapper plus local registry metadata in `artifacts/model_registry.json`.
- Added Dockerfiles for API and dashboard services.
- Expanded Docker Compose to run API and dashboard along with Postgres, Redis, Kafka, and MLflow.
- Removed generated Python cache files from the distributable ZIP.
