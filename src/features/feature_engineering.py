import pandas as pd


def add_behavioral_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "transaction_hour" in out.columns:
        out["is_night_transaction"] = out["transaction_hour"].between(0, 5).astype(int)
    if "amount" in out.columns and "customer_avg_amount_30d" in out.columns:
        out["amount_to_avg_ratio"] = (out["amount"] / out["customer_avg_amount_30d"].clip(lower=1)).round(4)
    if "merchant_risk_score" in out.columns:
        out["is_high_risk_merchant"] = (out["merchant_risk_score"] >= 2).astype(int)
    return out


def feature_columns(df: pd.DataFrame):
    return [c for c in df.columns if c not in {"transaction_id", "customer_id", "is_fraud"}]
