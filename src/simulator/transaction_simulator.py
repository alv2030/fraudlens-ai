from datetime import datetime, timezone
import random
import uuid

MERCHANTS = ["grocery", "travel", "electronics", "crypto", "restaurant", "fuel", "luxury", "gaming"]
COUNTRIES = ["US", "US", "US", "CA", "MX", "JP", "GB", "NG", "BR"]
DEVICES = ["ios", "android", "web", "unknown"]


def generate_transaction() -> dict:
    scenario = random.choices(
        population=["normal", "medium_risk", "high_risk"],
        weights=[0.70, 0.20, 0.10],
        k=1,
    )[0]

    if scenario == "high_risk":
        base_avg = round(random.uniform(20, 80), 2)
        amount = round(base_avg * random.uniform(5.5, 12.0), 2)
        merchant = random.choice(["crypto", "luxury", "gaming"])
        country = random.choice(["NG", "BR", "JP", "GB", "MX"])
        is_new_device = 1
        is_card_not_present = 1
        velocity_1h = random.randint(5, 10)
        merchant_risk_score = 2
        avg = base_avg

    elif scenario == "medium_risk":
        base_avg = round(random.uniform(25, 100), 2)
        amount = round(base_avg * random.uniform(2.0, 5.0), 2)
        merchant = random.choice(["travel", "electronics", "crypto", "luxury"])
        country = random.choice(["US", "CA", "MX", "GB", "JP"])
        is_new_device = int(random.random() < 0.45)
        is_card_not_present = int(random.random() < 0.65)
        velocity_1h = random.randint(2, 6)
        merchant_risk_score = 2 if merchant in {"crypto", "luxury", "gaming"} else 1
        avg = base_avg

    else:
        amount = round(random.lognormvariate(3.2, 0.8), 2)
        merchant = random.choice(["grocery", "restaurant", "fuel", "electronics"])
        country = random.choice(["US", "US", "US", "CA"])
        is_new_device = int(random.random() < 0.10)
        is_card_not_present = int(random.random() < 0.25)
        velocity_1h = random.randint(0, 3)
        merchant_risk_score = random.choice([0, 0, 1])
        avg = max(15.0, round(amount / random.uniform(0.8, 3.0), 2))

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": str(random.randint(10000, 19999)),
        "amount": amount,
        "transaction_hour": datetime.now().hour,
        "merchant_category": merchant,
        "merchant_risk_score": merchant_risk_score,
        "merchant_country": country,
        "device_type": random.choice(DEVICES),
        "is_foreign_transaction": int(country != "US"),
        "is_new_device": is_new_device,
        "is_card_not_present": is_card_not_present,
        "velocity_1h": velocity_1h,
        "customer_avg_amount_30d": avg,
        "scenario": scenario,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }