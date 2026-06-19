from pathlib import Path
from src.models.predict import score_transaction


def test_prediction_bootstraps_demo_model(tmp_path, monkeypatch):
    model_path = tmp_path / "fraud_model.joblib"
    monkeypatch.setattr("src.config.settings.settings.model_path", str(model_path))
    score = score_transaction({
        "transaction_id": "test_txn_001",
        "customer_id": "10001",
        "amount": 900.0,
        "transaction_hour": 2,
        "is_foreign_transaction": 1,
        "is_new_device": 1,
        "is_card_not_present": 1,
        "velocity_1h": 5,
        "merchant_risk_score": 2,
        "customer_avg_amount_30d": 80.0,
    })
    assert 0 <= score["fraud_probability"] <= 1
    assert 0 <= score["final_risk_score"] <= 100
    assert score["risk_level"] in {"LOW", "MEDIUM", "HIGH"}
