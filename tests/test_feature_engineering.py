import pandas as pd
from src.features.feature_engineering import add_behavioral_features


def test_add_behavioral_features():
    df = pd.DataFrame({"amount": [500], "customer_avg_amount_30d": [100], "transaction_hour": [2], "merchant_risk_score": [2]})
    out = add_behavioral_features(df)
    assert out.loc[0, "amount_to_avg_ratio"] == 5
    assert out.loc[0, "is_night_transaction"] == 1
    assert out.loc[0, "is_high_risk_merchant"] == 1
