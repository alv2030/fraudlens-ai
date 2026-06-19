from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health_contract():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_score_contract():
    payload = {
        "transaction_id": "txn_demo_001",
        "customer_id": "cust_123",
        "amount": 950.0,
        "merchant_category": "electronics",
        "merchant_risk_score": 0.82,
        "country": "US",
        "customer_home_country": "US",
        "is_card_present": False,
        "is_new_device": True,
        "transaction_hour": 2,
        "velocity_1h": 7,
        "avg_customer_amount": 120.0,
    }
    response = client.post("/score", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["transaction_id"] == "txn_demo_001"
    assert 0 <= body["final_score"] <= 1
    assert body["decision"] in {"approve", "review"}
    assert isinstance(body["reasons"], list)
