from __future__ import annotations

from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from src.data.load_data import generate_demo_dataset
from src.features.feature_engineering import add_behavioral_features, feature_columns
from src.data.preprocess import train_test
from src.config.settings import settings
from src.models.model_registry import register_model


def seed_demo_model(force: bool = False) -> Path:
    """Create a small demo model so API/dashboard can score immediately.

    This is not the final trained model. It is a resilient local fallback for demos,
    Docker startup, and reviewer inspection before running `make train`.
    """
    out = Path(settings.model_path)
    if out.exists() and not force:
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    df = generate_demo_dataset(n=8000, fraud_rate=0.01, seed=7)
    df = add_behavioral_features(df)
    X_train, X_test, y_train, y_test = train_test(df)
    model = RandomForestClassifier(n_estimators=80, max_depth=8, class_weight='balanced', random_state=7, n_jobs=-1)
    model.fit(X_train, y_train)
    package = {
        'model': model,
        'features': list(X_train.columns),
        'metrics': {'demo_seed_model': 1.0},
        'model_name': 'demo_random_forest_seed',
    }
    joblib.dump(package, out)
    register_model('demo_random_forest_seed', package['metrics'], str(out), stage='Production')
    return out

if __name__ == '__main__':
    print(seed_demo_model(force=True))
