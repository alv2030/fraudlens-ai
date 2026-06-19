from pathlib import Path
import json
import joblib
import mlflow
import pandas as pd
from sklearn.metrics import average_precision_score, precision_recall_fscore_support, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from xgboost import XGBClassifier
from src.config.settings import settings
from src.data.load_data import load_or_generate
from src.data.validate_data import validate_transactions
from src.data.preprocess import train_test
from src.features.feature_engineering import add_behavioral_features
from src.models.model_registry import register_model

ARTIFACT_DIR = Path("artifacts/models")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def evaluate(model, X_test, y_test, threshold=0.42):
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= threshold).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, pred, average="binary", zero_division=0)
    return {
        "roc_auc": float(roc_auc_score(y_test, prob)),
        "pr_auc": float(average_precision_score(y_test, prob)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "threshold": threshold,
    }


def train():
    df = load_or_generate(generate_demo=False)
    df = add_behavioral_features(df)
    validate_transactions(df)
    X_train, X_test, y_train, y_test = train_test(df)

    pos = max(int(y_train.sum()), 1)
    neg = len(y_train) - pos
    scale_pos_weight = neg / pos

    models = {
        "logistic_regression": LogisticRegression(max_iter=500, class_weight="balanced"),
        "random_forest": RandomForestClassifier(n_estimators=120, class_weight="balanced", random_state=42, n_jobs=-1),
        "xgboost": XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            scale_pos_weight=scale_pos_weight,
            random_state=42,
        ),
    }

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    best_name, best_model, best_metrics, best_run_id = None, None, None, None
    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            model.fit(X_train, y_train)
            metrics = evaluate(model, X_test, y_test, threshold=settings.threshold)
            mlflow.log_params(model.get_params())
            mlflow.log_metrics(metrics)
            if name == "xgboost":
                mlflow.sklearn.log_model(model, artifact_path="model")
            if best_metrics is None or metrics["pr_auc"] > best_metrics["pr_auc"]:
                best_name, best_model, best_metrics = name, model, metrics
                best_run_id = mlflow.active_run().info.run_id

    package = {"model": best_model, "features": list(X_train.columns), "metrics": best_metrics, "model_name": best_name}
    out = ARTIFACT_DIR / "fraud_model.joblib"
    joblib.dump(package, out)
    registry_record = register_model(best_name, best_metrics, str(out), run_id=best_run_id)
    Path("reports").mkdir(exist_ok=True)
    report = "# Model Performance\n\n" + json.dumps({"best_model": best_name, **best_metrics, "registry": registry_record}, indent=2)
    Path("reports/model_performance.md").write_text(report, encoding="utf-8")

if __name__ == "__main__":
    train()
