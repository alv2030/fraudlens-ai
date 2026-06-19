from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(default="postgresql+psycopg2://fraudlens:fraudlens@localhost:5432/fraudlens")
    redis_host: str = "localhost"
    redis_port: int = 6379
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "transactions"
    model_path: str = "artifacts/models/fraud_model.joblib"
    threshold: float = 0.42
    mlflow_tracking_uri: str = "http://localhost:5000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
