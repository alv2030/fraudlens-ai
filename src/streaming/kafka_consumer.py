import json
from kafka import KafkaConsumer
from src.config.settings import settings
from src.models.predict import score_transaction
from src.models.explain import simple_explanation


def run() -> None:
    consumer = KafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        group_id="fraudlens-scorer",
    )
    print("Fraud scoring consumer started")
    for msg in consumer:
        txn = msg.value
        score = score_transaction(txn)
        score["explanation"] = simple_explanation(txn, score["reasons"])
        print(json.dumps(score, indent=2))

if __name__ == "__main__":
    run()
