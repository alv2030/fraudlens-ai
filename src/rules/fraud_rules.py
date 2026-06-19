from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class RuleResult:
    score: float
    reasons: List[str]


def calculate_rule_score(txn: Dict) -> RuleResult:
    score = 0.0
    reasons: List[str] = []

    amount = float(txn.get("amount", 0))
    avg = max(float(txn.get("customer_avg_amount_30d", 1)), 1)
    ratio = amount / avg

    if ratio >= 5:
        score += 25
        reasons.append(f"Amount is {ratio:.1f}x higher than customer average")
    if int(txn.get("is_foreign_transaction", 0)) == 1:
        score += 20
        reasons.append("Foreign transaction")
    if int(txn.get("is_new_device", 0)) == 1:
        score += 15
        reasons.append("New device")
    if int(txn.get("velocity_1h", 0)) >= 5:
        score += 20
        reasons.append("High transaction velocity within one hour")
    if int(txn.get("is_card_not_present", 0)) == 1:
        score += 10
        reasons.append("Card-not-present transaction")
    if int(txn.get("merchant_risk_score", 0)) >= 2:
        score += 10
        reasons.append("High-risk merchant category")

    return RuleResult(score=min(score, 100.0), reasons=reasons)


def risk_level(score: float) -> str:
    if score >= 71:
        return "HIGH"
    if score >= 41:
        return "MEDIUM"
    return "LOW"
