# Bruin Project: Olist Revenue Analytics

## Problem Description
Olist wants to see how payment methods and delivery delays affect revenue. The first version of this project was more manual. This Bruin version ties the steps together into one ETL/ELT pipeline so the results are easier to rerun and share.

## What This Project Does
- Ingests Olist data from Kaggle into a raw landing zone.
- Uploads raw CSVs to an S3-compatible data lake.
- Loads raw data into Snowflake tables.
- Builds analytics tables (`olist_orders_cleaned`, `fact_sales`) optimized for time-series queries.
- Optional dbt run for transformations (reuses the existing `dbt/` project).
- Streams payment records through Kafka (producer and consumer) as an optional real-time extension.
- Feeds dashboards (Streamlit or Power BI) with monthly revenue and payment-type breakdowns.

## Project Structure
- `bruin.yml`: Bruin project config and environments.
- `assets/ingest/`: Batch ingestion assets (Kaggle download, lake upload).
- `assets/warehouse/`: Snowflake staging and load SQL.
- `assets/transform/`: Analytics transformations (cleaned orders, fact sales).
- `assets/streaming/`: Kafka producer and consumer for real-time payments.
- `streaming/docker-compose.yml`: Redpanda (Kafka-compatible) for local streaming.

## Cloud + IaC
- Cloud warehouse: Snowflake (prod environment in `bruin.yml`).
- Cloud data lake: S3-compatible bucket (AWS S3 or MinIO).
- IaC: Terraform skeleton in `infra/terraform/` provisions the bucket and related resources.

## How To Run
1. Install dependencies.
   - `pip install -r bruin/requirements.txt`
2. Set environment variables for Snowflake and the lake (see `bruin.yml`).
   - Use `bruin/.env.example` as a template.
3. Run batch assets in order.
   - Example sequence: `ingest_olist_kaggle` -> `ingest_olist_to_lake` -> `stage_olist_tables` -> `load_olist_tables` -> `transform_olist_orders_cleaned` -> `transform_fact_sales`
   - Optional: `transform_dbt_run` instead of the SQL transform assets.
4. Optional: start streaming.
   - `docker compose -f bruin/streaming/docker-compose.yml up -d`
   - Run `assets/streaming/payments_producer.py` then `assets/streaming/payments_consumer.py`
5. Run dashboards.
   - Streamlit: `streamlit run dashboard/streamlit_app.py`
   - Power BI: follow `dashboard/powerbi/README.md`

## Notes
- Batch orchestration is implemented as a Bruin DAG via asset dependencies.
- `fact_sales` is clustered by `purchase_at` to improve time-series queries.
- Streaming assets are optional and do not affect the batch pipeline.
