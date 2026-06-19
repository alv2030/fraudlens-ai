import pandas as pd

from src.data.validation import validate_transactions


def test_validation_detects_negative_amount():
    df = pd.DataFrame({"amount": [-1], "merchant_risk_score": [0.5], "transaction_hour": [12]})
    errors = validate_transactions(df)
    assert "amount_contains_negative_values" in errors
