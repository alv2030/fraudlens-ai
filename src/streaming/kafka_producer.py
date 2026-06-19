import json
import time
from kafka import KafkaProducer
from src.config.settings import settings
from src.simulator.transaction_simulator import generate_transaction


def run() -> None:
    producer = KafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    print(f"Producing transactions to topic={settings.kafka_topic}")
    while True:
        txn = generate_transaction()
        producer.send(settings.kafka_topic, txn)
        producer.flush()
        print(txn)
        time.sleep(2)

if __name__ == "__main__":
    run()
