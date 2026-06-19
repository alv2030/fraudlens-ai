from fastapi import APIRouter, HTTPException, Query
from src.api.schemas import AlertUpdateRequest, TransactionRequest, ScoreResponse
from src.models.predict import score_transaction
from src.data.database import (
    create_alert_if_needed,
    insert_prediction,
    insert_transaction,
    list_alerts,
    update_alert_status,
    init_db,
)

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "fraudlens-ai-v2"}

@router.post("/admin/init-db")
def initialize_database():
    try:
        init_db()
        return {"status": "ok", "message": "Database schema initialized."}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Unable to initialize database: {exc}") from exc

@router.post("/admin/seed-model")
def seed_model():
    from src.models.seed_model import seed_demo_model
    path = seed_demo_model(force=True)
    return {"status": "ok", "model_path": str(path)}

@router.post("/score-transaction", response_model=ScoreResponse)
def score(request: TransactionRequest, persist: bool = Query(default=False)):
    txn = request.model_dump()
    result = score_transaction(txn)
    if persist:
        try:
            insert_transaction(txn)
            insert_prediction(result)
            alert_id = create_alert_if_needed(result)
            result["alert_id"] = alert_id
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"Scored transaction but failed to persist: {exc}") from exc
    return result

@router.get("/alerts")
def alerts(status: str | None = None, limit: int = 100):
    try:
        return {"alerts": list_alerts(status=status, limit=limit)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Unable to read alerts from PostgreSQL: {exc}") from exc

@router.patch("/alerts/{alert_id}/status")
def update_alert(alert_id: int, request: AlertUpdateRequest):
    try:
        return update_alert_status(alert_id, request.status, request.changed_by, request.notes)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Unable to update alert: {exc}") from exc

@router.get("/model-performance")
def model_performance():
    import json
    from pathlib import Path
    registry = Path("artifacts/model_registry.json")
    report = Path("reports/model_performance.md")
    return {
        "registry": json.loads(registry.read_text()) if registry.exists() else [],
        "report_path": str(report),
        "message": "Run `make train` to refresh model metrics." if not report.exists() else report.read_text(encoding="utf-8")[:4000],
    }
