SELECT
  customer_id,
  customer_city,
  customer_state
FROM read_csv_auto(
  '{{ var("data_path", "../data/landing") }}/olist_customers_dataset.csv',
  header=true
)
