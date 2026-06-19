from src.streaming.spark_streaming_job import TRANSACTION_FIELDS


def test_streaming_schema_contains_required_fields():
    assert "transaction_id" in TRANSACTION_FIELDS
    assert "amount" in TRANSACTION_FIELDS
    assert "customer_avg_amount_30d" in TRANSACTION_FIELDS
