-- Cleaned orders with typed timestamps.
CREATE OR REPLACE TABLE olist_orders_cleaned AS
SELECT
  order_id,
  customer_id,
  order_status,
  TO_TIMESTAMP(order_purchase_timestamp) AS purchase_at,
  TO_TIMESTAMP(order_delivered_customer_date) AS delivered_at
FROM olist_orders;
