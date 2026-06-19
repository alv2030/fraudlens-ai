import pandas as pd

REQUIRED_COLUMNS = ["amount", "is_fraud"]


def validate_transactions(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if df["amount"].isna().any():
        raise ValueError("amount contains null values")
    if (df["amount"] < 0).any():
        raise ValueError("amount contains negative values")
    if not set(df["is_fraud"].dropna().unique()).issubset({0, 1}):
        raise ValueError("is_fraud must be binary")
