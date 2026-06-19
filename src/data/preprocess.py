from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

TARGET = "is_fraud"
DROP_COLUMNS = ["transaction_id"]


def split_features_target(df: pd.DataFrame):
    X = df.drop(columns=[TARGET] + [c for c in DROP_COLUMNS if c in df.columns])
    X = pd.get_dummies(X, drop_first=True)
    y = df[TARGET].astype(int)
    return X, y


def train_test(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X, y = split_features_target(df)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
