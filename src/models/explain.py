from __future__ import annotations

from typing import Any
import numpy as np
import pandas as pd


def simple_explanation(txn: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    return {
        "top_reasons": reasons[:5],
        "summary": "Transaction was flagged because behavioral and contextual risk signals exceeded the scoring threshold." if reasons else "No major rule-based risk drivers detected.",
    }


def shap_explanation(model: Any, features_df: pd.DataFrame, fallback_reasons: list[str]) -> dict[str, Any]:
    """Return lightweight SHAP-style drivers for one transaction.

    Uses real SHAP TreeExplainer when available. If SHAP is unavailable or the model
    is incompatible, returns rule-based drivers instead so the API remains reliable.
    """
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(features_df)
        if isinstance(values, list):
            values = values[-1]
        arr = np.asarray(values)
        if arr.ndim == 2:
            arr = arr[0]
        pairs = sorted(zip(features_df.columns, arr), key=lambda item: abs(float(item[1])), reverse=True)[:5]
        return {
            "method": "shap_tree_explainer",
            "top_features": [{"feature": name, "impact": round(float(value), 6)} for name, value in pairs],
            "rule_reasons": fallback_reasons[:5],
        }
    except Exception:
        return {
            "method": "rule_fallback",
            "top_features": [],
            "rule_reasons": fallback_reasons[:5],
            "summary": simple_explanation({}, fallback_reasons)["summary"],
        }
