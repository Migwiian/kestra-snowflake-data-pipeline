-- Snowflake staging objects for Olist raw CSVs.
-- Replace the URL and credentials with your storage integration or external stage details.
CREATE OR REPLACE FILE FORMAT olist_csv
  TYPE = 'CSV'
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1;

-- Example external stage:
-- CREATE OR REPLACE STAGE olist_stage
--   URL = 's3://<LAKE_BUCKET>/olist/raw'
--   STORAGE_INTEGRATION = <STORAGE_INTEGRATION>
--   FILE_FORMAT = olist_csv;

CREATE OR REPLACE STAGE olist_stage
  FILE_FORMAT = olist_csv;

CREATE OR REPLACE TABLE olist_orders (
  order_id STRING,
  customer_id STRING,
  order_status STRING,
  order_purchase_timestamp STRING,
  order_delivered_customer_date STRING
);

CREATE OR REPLACE TABLE olist_customers (
  customer_id STRING,
  customer_unique_id STRING,
  customer_zip_code_prefix STRING,
  customer_city STRING,
  customer_state STRING
);

CREATE OR REPLACE TABLE olist_order_payments (
  order_id STRING,
  payment_sequential STRING,
  payment_type STRING,
  payment_installments STRING,
  payment_value STRING
);
