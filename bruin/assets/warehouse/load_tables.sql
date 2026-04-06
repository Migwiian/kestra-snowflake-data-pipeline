-- Load raw CSVs from stage into Snowflake tables.
COPY INTO olist_orders
  FROM @olist_stage/olist_orders_dataset.csv
  FILE_FORMAT = (FORMAT_NAME = olist_csv)
  ON_ERROR = 'CONTINUE';

COPY INTO olist_customers
  FROM @olist_stage/olist_customers_dataset.csv
  FILE_FORMAT = (FORMAT_NAME = olist_csv)
  ON_ERROR = 'CONTINUE';

COPY INTO olist_order_payments
  FROM @olist_stage/olist_order_payments_dataset.csv
  FILE_FORMAT = (FORMAT_NAME = olist_csv)
  ON_ERROR = 'CONTINUE';
