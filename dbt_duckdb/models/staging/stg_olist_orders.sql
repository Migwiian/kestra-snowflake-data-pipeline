SELECT
  order_id,
  customer_id,
  order_status,
  order_purchase_timestamp,
  order_delivered_customer_date,
  order_estimated_delivery_date
FROM read_csv_auto(
  '{{ var("data_path", "../data/landing") }}/olist_orders_dataset.csv',
  header=true
)
