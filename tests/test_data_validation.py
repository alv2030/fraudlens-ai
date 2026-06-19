import pandas as pd
import pytest
from src.data.validate_data import validate_transactions


def test_validation_passes():
    validate_transactions(pd.DataFrame({"amount": [10], "is_fraud": [0]}))


def test_validation_negative_amount():
    with pytest.raises(ValueError):
        validate_transactions(pd.DataFrame({"amount": [-1], "is_fraud": [0]}))
