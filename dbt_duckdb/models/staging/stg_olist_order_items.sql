SELECT
  order_id,
  price,
  freight_value
FROM read_csv_auto(
  '{{ var("data_path", "../data/landing") }}/olist_order_items_dataset.csv',
  header=true
)
