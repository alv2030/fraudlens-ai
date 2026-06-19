import json
from typing import Any, Dict
import redis
from src.config.settings import settings

class FeatureStore:
    def __init__(self):
        self.client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)

    def get_customer_features(self, customer_id: str) -> Dict[str, Any]:
        raw = self.client.get(f"customer:{customer_id}")
        if raw:
            return json.loads(raw)
        return {
            "customer_avg_amount_30d": 75.0,
            "customer_transaction_count_24h": 1,
            "customer_home_country": "US",
            "known_devices": [],
        }

    def set_customer_features(self, customer_id: str, features: Dict[str, Any]) -> None:
        self.client.set(f"customer:{customer_id}", json.dumps(features), ex=60 * 60 * 24)
