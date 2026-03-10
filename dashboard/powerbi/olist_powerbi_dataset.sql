SELECT
  payment_type,
  DATE_TRUNC('month', purchase_at) AS purchase_month,
  COUNT(DISTINCT order_id) AS order_count,
  SUM(payment_value_total) AS total_revenue
FROM powerbi_dataset
GROUP BY 1, 2
ORDER BY 2, 1;
