from datetime import datetime, timezone
import random
import uuid

MERCHANTS = ["grocery", "travel", "electronics", "crypto", "restaurant", "fuel", "luxury", "gaming"]
COUNTRIES = ["US", "US", "US", "CA", "MX", "JP", "GB", "NG", "BR"]
DEVICES = ["ios", "android", "web", "unknown"]


def generate_transaction() -> dict:
    amount = round(random.lognormvariate(3.2, 1.0), 2)
    merchant = random.choice(MERCHANTS)
    country = random.choice(COUNTRIES)
    avg = max(15.0, round(amount / random.uniform(0.4, 4.0), 2))
    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": str(random.randint(10000, 19999)),
        "amount": amount,
        "transaction_hour": datetime.now().hour,
        "merchant_category": merchant,
        "merchant_risk_score": 2 if merchant in {"crypto", "luxury", "gaming"} else random.choice([0, 1]),
        "merchant_country": country,
        "device_type": random.choice(DEVICES),
        "is_foreign_transaction": int(country != "US"),
        "is_new_device": random.binomialvariate(1, 0.15) if hasattr(random, 'binomialvariate') else int(random.random() < 0.15),
        "is_card_not_present": int(random.random() < 0.35),
        "velocity_1h": random.randint(0, 8),
        "customer_avg_amount_30d": avg,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
