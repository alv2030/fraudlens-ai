from typing import Optional, Literal
from pydantic import BaseModel, Field

class TransactionRequest(BaseModel):
    transaction_id: Optional[str] = None
    customer_id: str = "10001"
    amount: float = Field(gt=0)
    transaction_hour: int = Field(default=12, ge=0, le=23)
    is_foreign_transaction: int = 0
    is_new_device: int = 0
    is_card_not_present: int = 0
    velocity_1h: int = 1
    merchant_risk_score: int = 0
    customer_avg_amount_30d: float = 75.0
    merchant_category: str = "unknown"
    merchant_country: str = "US"
    device_type: str = "unknown"

class ScoreResponse(BaseModel):
    transaction_id: Optional[str]
    fraud_probability: float
    rule_score: float
    final_risk_score: float
    risk_level: str
    prediction_label: int
    reasons: list[str]
    shap_explanation: dict
    model_version: str
    alert_id: Optional[int] = None

class AlertUpdateRequest(BaseModel):
    status: Literal["OPEN", "UNDER_REVIEW", "CONFIRMED_FRAUD", "FALSE_POSITIVE", "CLOSED"]
    changed_by: str = "analyst"
    notes: Optional[str] = None
