import argparse
from pathlib import Path
import numpy as np
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def generate_demo_dataset(n: int = 120_000, fraud_rate: float = 0.006, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    amount = rng.lognormal(mean=3.2, sigma=1.1, size=n).round(2)
    hour = rng.integers(0, 24, size=n)
    foreign = rng.binomial(1, 0.08, size=n)
    new_device = rng.binomial(1, 0.12, size=n)
    card_not_present = rng.binomial(1, 0.35, size=n)
    velocity_1h = rng.poisson(1.2, size=n)
    merchant_risk = rng.choice([0, 1, 2], size=n, p=[0.72, 0.22, 0.06])

    risk_logit = (
        -6.2
        + 0.7 * (amount > np.quantile(amount, 0.95))
        + 1.2 * foreign
        + 1.1 * new_device
        + 0.5 * card_not_present
        + 0.4 * (hour <= 5)
        + 0.45 * (velocity_1h >= 4)
        + 0.8 * merchant_risk
    )
    prob = 1 / (1 + np.exp(-risk_logit))
    # scale probability to target approximate fraud rate
    prob = prob * (fraud_rate / prob.mean())
    y = rng.binomial(1, np.clip(prob, 0, 0.95))

    df = pd.DataFrame({
        "transaction_id": [f"txn_{i:08d}" for i in range(n)],
        "customer_id": rng.integers(10000, 19999, size=n),
        "amount": amount,
        "transaction_hour": hour,
        "is_foreign_transaction": foreign,
        "is_new_device": new_device,
        "is_card_not_present": card_not_present,
        "velocity_1h": velocity_1h,
        "merchant_risk_score": merchant_risk,
        "is_fraud": y,
    })
    df["customer_avg_amount_30d"] = np.maximum(10, df["amount"] / rng.uniform(0.3, 3.5, size=n)).round(2)
    df["amount_to_avg_ratio"] = (df["amount"] / df["customer_avg_amount_30d"]).round(3)
    return df


def load_or_generate(generate_demo: bool = False) -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    kaggle = RAW_DIR / "creditcard.csv"
    if kaggle.exists() and not generate_demo:
        df = pd.read_csv(kaggle)
        # Kaggle uses Amount and Class columns. Normalize names.
        df = df.rename(columns={"Amount": "amount", "Class": "is_fraud"})
        return df
    return generate_demo_dataset()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-demo", action="store_true")
    args = parser.parse_args()
    df = load_or_generate(generate_demo=args.generate_demo)
    out = PROCESSED_DIR / "transactions.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df):,} rows to {out}")
    print(f"Fraud rate: {df['is_fraud'].mean():.4%}")

if __name__ == "__main__":
    main()
