# AWS Deployment Plan

Simplest realistic deployment:

1. Build Docker images in GitHub Actions.
2. Push images to AWS ECR.
3. Deploy FastAPI and Streamlit services to ECS Fargate.
4. Use RDS PostgreSQL for persistence.
5. Use CloudWatch for logs and alarms.

This folder intentionally contains templates/placeholders only until real AWS resources are created.
