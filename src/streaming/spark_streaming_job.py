"""Spark Structured Streaming job for Kafka fraud scoring.

v2 adds a real sink path: each micro-batch can be scored with the same ML/rule
engine and persisted to PostgreSQL as transactions, predictions, and alerts.
A console sink remains available for quick demos.
"""
from __future__ import annotations

import argparse
import json
from typing import Iterable

from src.config.settings import settings
from src.models.predict import score_transaction
from src.data.database import init_db, persist_scored_transaction

TRANSACTION_FIELDS = [
    "transaction_id", "customer_id", "amount", "transaction_hour",
    "is_foreign_transaction", "is_new_device", "is_card_not_present",
    "velocity_1h", "merchant_risk_score", "customer_avg_amount_30d",
    "merchant_category", "merchant_country", "device_type",
]


def score_and_persist_records(records: Iterable[dict]) -> int:
    """Score a batch of transaction dictionaries and persist them to PostgreSQL."""
    count = 0
    init_db()
    for txn in records:
        clean_txn = {k: txn.get(k) for k in TRANSACTION_FIELDS if k in txn}
        if not clean_txn.get("transaction_id"):
            continue
        score = score_transaction(clean_txn)
        persist_scored_transaction(clean_txn, score)
        count += 1
    return count


def foreach_batch_to_postgres(batch_df, batch_id: int) -> None:
    rows = [json.loads(row["value"]) if isinstance(row["value"], str) else row.asDict() for row in batch_df.collect()]
    processed = score_and_persist_records(rows)
    print(f"Processed Spark micro-batch {batch_id}: {processed} records persisted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Validate job wiring without connecting to Kafka.")
    parser.add_argument("--sink", choices=["postgres", "console"], default="postgres")
    args = parser.parse_args()

    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
    except Exception as exc:
        if args.dry_run:
            print("PySpark unavailable, but job module imported successfully:", exc)
            return
        raise

    spark = SparkSession.builder.appName("FraudLensV2SparkStreaming").getOrCreate()
    if args.dry_run:
        print("Spark Structured Streaming configured")
        print("Kafka bootstrap:", settings.kafka_bootstrap_servers)
        print("Kafka topic:", settings.kafka_topic)
        print("Sink:", args.sink)
        spark.stop()
        return

    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", settings.kafka_bootstrap_servers)
        .option("subscribe", settings.kafka_topic)
        .option("startingOffsets", "latest")
        .load()
    )
    values = raw.select(col("value").cast("string").alias("value"))

    if args.sink == "console":
        query = values.writeStream.format("console").option("truncate", "false").outputMode("append").start()
    else:
        query = values.writeStream.foreachBatch(foreach_batch_to_postgres).outputMode("append").start()
    query.awaitTermination()


if __name__ == "__main__":
    main()
