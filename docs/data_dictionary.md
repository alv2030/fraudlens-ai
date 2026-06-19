# Data Dictionary

| Field | Meaning |
|---|---|
| transaction_id | Unique transaction identifier |
| customer_id | Customer identifier |
| amount | Transaction amount |
| merchant_category | Merchant category label |
| merchant_risk_score | Risk score from merchant history/simulation |
| country | Transaction country |
| customer_home_country | Customer usual country |
| is_card_present | Whether physical card was present |
| is_new_device | Whether device is new for customer |
| transaction_hour | Local transaction hour, 0-23 |
| velocity_1h | Transactions by customer in last hour |
| avg_customer_amount | Historical average customer transaction amount |
| is_fraud | Training label |
