SELECT
  order_id,
  payment_type,
  payment_value
FROM read_csv_auto(
  '{{ var("data_path", "../data/landing") }}/olist_order_payments_dataset.csv',
  header=true
)
