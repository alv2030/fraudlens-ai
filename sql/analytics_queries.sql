-- Daily fraud alert volume
SELECT DATE(created_at) AS alert_date, COUNT(*) AS alerts
FROM fraud_alerts
GROUP BY DATE(created_at)
ORDER BY alert_date DESC;

-- Highest risk transactions
SELECT transaction_id, fraud_probability, rule_score, final_risk_score, scored_at
FROM fraud_predictions
ORDER BY final_risk_score DESC
LIMIT 20;
