from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Any
import json
try:
    import mlflow
    from mlflow.tracking import MlflowClient
except Exception:  # MLflow is optional for lightweight tests/local inspection
    mlflow = None
    MlflowClient = None
from src.config.settings import settings

REGISTRY_PATH = Path("artifacts/model_registry.json")


def _read_local_registry() -> list[dict[str, Any]]:
    if not REGISTRY_PATH.exists():
        return []
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def register_model(model_name: str, metrics: dict[str, float], artifact_path: str, run_id: str | None = None, stage: str = "Production") -> dict[str, Any]:
    """Register a model in MLflow when available and mirror metadata locally.

    The local JSON registry makes this project usable without a running MLflow server,
    while MLflow registration demonstrates the production model lifecycle.
    """
    records = _read_local_registry()
    version = len([r for r in records if r.get("model_name") == model_name]) + 1
    mlflow_model_uri = None
    mlflow_registered_version = None

    if run_id and mlflow is not None and MlflowClient is not None:
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            client = MlflowClient()
            registered = mlflow.register_model(f"runs:/{run_id}/model", model_name)
            mlflow_model_uri = f"models:/{model_name}/{registered.version}"
            mlflow_registered_version = registered.version
            # Transition stage is deprecated in newer MLflow, but still useful in many setups.
            try:
                client.transition_model_version_stage(model_name, registered.version, stage=stage, archive_existing_versions=True)
            except Exception:
                pass
        except Exception:
            mlflow_model_uri = None

    record = {
        "model_name": model_name,
        "version": version,
        "stage": stage,
        "metrics": metrics,
        "artifact_path": artifact_path,
        "mlflow_model_uri": mlflow_model_uri,
        "mlflow_registered_version": mlflow_registered_version,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    records.append(record)
    REGISTRY_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return record


def latest_production_model() -> dict[str, Any] | None:
    records = [r for r in _read_local_registry() if r.get("stage") == "Production"]
    return records[-1] if records else None
