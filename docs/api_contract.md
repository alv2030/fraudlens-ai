# API Contract

## GET /health

Returns service status.

## POST /score

Scores one transaction.

Required fields:

- transaction_id
- customer_id
- amount
- merchant_category
- merchant_risk_score
- country
- customer_home_country
- is_card_present
- is_new_device
- transaction_hour
- velocity_1h
- avg_customer_amount

Response fields:

- fraud_probability
- rule_score
- final_score
- decision
- threshold
- reasons

## GET /alerts

Returns demo alert list. Production persistence is represented by SQL schema.
