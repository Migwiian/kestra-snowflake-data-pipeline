WITH orders_cleaned AS (
  SELECT
    order_id,
    customer_id,
    order_status,
    TO_TIMESTAMP(order_purchase_timestamp) AS purchase_at,
    TO_TIMESTAMP(order_delivered_customer_date) AS delivered_at,
    TO_TIMESTAMP(order_estimated_delivery_date) AS estimated_delivered_at
  FROM olist_orders
),

payments_agg AS (
  SELECT
    order_id,
    CASE
      WHEN COUNT(DISTINCT payment_type) = 1 THEN MIN(payment_type)
      ELSE 'multiple'
    END AS payment_type,
    SUM(CAST(payment_value AS FLOAT)) AS payment_value_total
  FROM olist_order_payments
  GROUP BY 1
),

items_agg AS (
  SELECT
    order_id,
    COUNT(*) AS items_count,
    SUM(CAST(price AS FLOAT)) AS items_value_total,
    SUM(CAST(freight_value AS FLOAT)) AS freight_value_total
  FROM olist_order_items
  GROUP BY 1
)

SELECT
  o.order_id,
  o.customer_id,
  o.order_status,
  o.purchase_at,
  o.delivered_at,
  o.estimated_delivered_at,
  CASE
    WHEN o.delivered_at IS NULL THEN NULL
    ELSE DATEDIFF('day', o.purchase_at, o.delivered_at)
  END AS delivery_days,
  CASE
    WHEN o.delivered_at IS NULL OR o.estimated_delivered_at IS NULL THEN NULL
    ELSE DATEDIFF('day', o.estimated_delivered_at, o.delivered_at)
  END AS delivery_delay_days,
  c.customer_city,
  c.customer_state,
  p.payment_type,
  p.payment_value_total,
  i.items_count,
  i.items_value_total,
  i.freight_value_total
FROM orders_cleaned o
LEFT JOIN olist_customers c ON o.customer_id = c.customer_id
LEFT JOIN payments_agg p ON o.order_id = p.order_id
LEFT JOIN items_agg i ON o.order_id = i.order_id
