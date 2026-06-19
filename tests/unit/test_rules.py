from app.api.schemas.transaction import TransactionRequest
from src.rules.fraud_rules import FraudRuleEngine


def test_high_risk_transaction_has_reasons():
    tx = TransactionRequest(
        transaction_id="txn_1",
        customer_id="cust_1",
        amount=1500,
        merchant_category="electronics",
        merchant_risk_score=0.9,
        country="CA",
        customer_home_country="US",
        is_card_present=False,
        is_new_device=True,
        transaction_hour=2,
        velocity_1h=8,
        avg_customer_amount=100,
    )
    score, reasons = FraudRuleEngine().evaluate(tx)
    assert score > 0.8
    assert "high_amount" in reasons
    assert "new_device" in reasons
