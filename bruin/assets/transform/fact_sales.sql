-- Gold layer fact table for revenue analytics.
CREATE OR REPLACE TABLE fact_sales AS
SELECT
  o.order_id,
  o.purchase_at,
  c.customer_city,
  c.customer_state,
  p.payment_type,
  CAST(p.payment_value AS FLOAT) AS total_order_value
FROM olist_orders_cleaned o
JOIN olist_customers c ON o.customer_id = c.customer_id
JOIN olist_order_payments p ON o.order_id = p.order_id;

-- Cluster by purchase date for time-series performance.
ALTER TABLE fact_sales CLUSTER BY (purchase_at);
