import pandas as pd

from src.features.build_features import FEATURE_COLUMNS, select_features


def test_feature_builder_outputs_expected_columns():
    df = pd.DataFrame([
        {
            "transaction_id": "txn_1",
            "customer_id": "cust_1",
            "amount": 500,
            "merchant_risk_score": 0.5,
            "country": "US",
            "customer_home_country": "CA",
            "is_card_present": False,
            "is_new_device": True,
            "transaction_hour": 3,
            "velocity_1h": 2,
            "avg_customer_amount": 100,
            "is_fraud": 1,
        }
    ])
    features = select_features(df)
    assert list(features.columns) == FEATURE_COLUMNS
    assert features.loc[0, "country_mismatch"] == 1
    assert features.loc[0, "is_late_night"] == 1
