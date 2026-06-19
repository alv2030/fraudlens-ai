CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(64) PRIMARY KEY,
    home_country VARCHAR(8),
    avg_amount_30d NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64),
    amount NUMERIC(12,2),
    merchant_category VARCHAR(64),
    merchant_country VARCHAR(8),
    device_type VARCHAR(64),
    card_present BOOLEAN,
    transaction_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transaction_features (
    transaction_id VARCHAR(64) PRIMARY KEY,
    amount_to_avg_ratio NUMERIC(12,4),
    velocity_1h INTEGER,
    velocity_24h INTEGER,
    is_foreign_transaction BOOLEAN,
    is_high_risk_merchant BOOLEAN,
    is_new_device BOOLEAN,
    is_night_transaction BOOLEAN
);

CREATE TABLE IF NOT EXISTS fraud_predictions (
    prediction_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(64),
    model_version VARCHAR(64),
    fraud_probability NUMERIC(8,6),
    rule_score NUMERIC(8,2),
    final_risk_score NUMERIC(8,2),
    prediction_label INTEGER,
    shap_explanation TEXT,
    scored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(64),
    risk_level VARCHAR(16),
    alert_status VARCHAR(32) DEFAULT 'OPEN',
    assigned_to VARCHAR(64),
    investigation_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_status_history (
    history_id SERIAL PRIMARY KEY,
    alert_id INTEGER,
    old_status VARCHAR(32),
    new_status VARCHAR(32),
    changed_by VARCHAR(64),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
