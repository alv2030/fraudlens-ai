from pathlib import Path
from typing import Dict
import joblib
import pandas as pd
from src.config.settings import settings
from src.features.feature_engineering import add_behavioral_features
from src.rules.fraud_rules import calculate_rule_score, risk_level
from src.models.explain import shap_explanation
from src.models.model_registry import latest_production_model


def load_model_package(path: str | None = None):
    registry_record = latest_production_model()
    p = Path(path or (registry_record or {}).get("artifact_path", settings.model_path))
    if not p.exists():
        p = Path(settings.model_path)
    if not p.exists():
        from src.models.seed_model import seed_demo_model
        p = seed_demo_model(force=False)
    return joblib.load(p)


def score_transaction(txn: Dict) -> Dict:
    package = load_model_package()
    model = package["model"]
    features = package["features"]
    df = pd.DataFrame([txn])
    df = add_behavioral_features(df)
    df = pd.get_dummies(df)
    for col in features:
        if col not in df.columns:
            df[col] = 0
    df = df[features]
    ml_prob = float(model.predict_proba(df)[0, 1])
    rule = calculate_rule_score({**txn, **df.iloc[0].to_dict()})
    final_score = round((ml_prob * 100 * 0.70) + (rule.score * 0.30), 2)
    explanation = shap_explanation(model, df, rule.reasons)
    return {
        "transaction_id": txn.get("transaction_id"),
        "fraud_probability": round(ml_prob, 4),
        "rule_score": round(rule.score, 2),
        "final_risk_score": final_score,
        "risk_level": risk_level(final_score),
        "prediction_label": int(final_score >= settings.threshold * 100),
        "reasons": rule.reasons,
        "shap_explanation": explanation,
        "model_version": package.get("model_name", "local-xgboost"),
    }
