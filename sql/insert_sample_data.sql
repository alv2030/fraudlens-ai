INSERT INTO customers (customer_id, home_country, avg_amount_30d)
VALUES ('10001', 'US', 72.50)
ON CONFLICT (customer_id) DO NOTHING;
