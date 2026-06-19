# FraudLens AI v2 Final Notes

This version is the recommended resume/GitHub version.

## Upgrades included

- Auto-seeded demo model for API and dashboard startup.
- FastAPI lifespan bootstrap for model artifact and database initialization.
- Real PostgreSQL alert workflow: transactions, predictions, alerts, status history.
- Spark Structured Streaming micro-batch sink path that scores and persists records.
- Dockerfile for streaming service in addition to API and dashboard.
- Docker Compose service for streaming dry-run/extension.
- Clear README wording that distinguishes demo/local system from real PCI-compliant production.
- Tests pass with `pytest -q`.

## Reviewer caveat

This is a portfolio-grade local ML engineering system. It demonstrates architecture and implementation patterns, but it is not a regulated banking production system.
