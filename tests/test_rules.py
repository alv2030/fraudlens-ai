from src.rules.fraud_rules import calculate_rule_score, risk_level


def test_high_risk_rules():
    txn = {
        "amount": 1000,
        "customer_avg_amount_30d": 100,
        "is_foreign_transaction": 1,
        "is_new_device": 1,
        "velocity_1h": 6,
        "is_card_not_present": 1,
        "merchant_risk_score": 2,
    }
    result = calculate_rule_score(txn)
    assert result.score == 100
    assert risk_level(result.score) == "HIGH"
