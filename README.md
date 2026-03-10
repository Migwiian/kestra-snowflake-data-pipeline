# Kestra Snowflake Olist Pipeline

## Executive Summary: Retail Revenue Optimization
**Business Problem:** A Brazilian e-commerce marketplace (Olist) needs to understand how payment methods and delivery delays impact revenue realization to optimize cash flow and customer retention.

**Solution:** An automated, production-grade data pipeline that transforms raw Kaggle data into a Snowflake analytics layer. Stakeholders can track monthly revenue trends and relate delivery performance to financial outcomes.

**Key Deliverables:**
- Automated ETL from Kaggle to Snowflake using Kestra.
- Analytics warehouse with Raw → Staging → Fact/Dim layers and clustered `fact_sales` for time-series performance.
- Streamlit dashboard for monthly revenue trends and payment-type distribution.

## Repository Layout
- `flows/olist_download.yml`: Downloads dataset and stores files in Kestra internal storage.
- `flows/olist_lake.yml`: Copies raw CSVs to a local MinIO (S3-compatible) data lake.
- `flows/snowflake_loader.yml`: Creates Snowflake objects and loads all CSVs.
- `flows/snowflake_transform.yml`: Builds analytical tables (`olist_orders_cleaned`, `fact_sales`). This stage implements a modular transformation layer, moving data from Raw (Bronze) staging tables to Analytical (Silver/Gold) fact and dimension tables.
- `flows/olist_pipeline.yml`: Orchestrates download → load → transform.
- `docker-compose.yml`: Runs Kestra and Postgres with local storage mounts.
- `Dockerfile`: Extends `kestra/kestra` with Python and Kaggle CLI.
- `dbt/`: Optional dbt project that mirrors the transformation logic.
- `dbt_duckdb/`: Parallel dbt project for Power BI using DuckDB + local CSVs (local track).
- `secrets.conf`: Source-of-truth credentials (plain text, local only).
- `.env`: Runtime configuration consumed by Docker/Kestra (plain text, local only).
- `infra/terraform/`: Optional Terraform skeleton to provision a cloud data lake bucket.

## Environment and Secret Management
This project follows Kestra's open-source secret handling: secrets are provided as base64-encoded environment variables prefixed with `SECRET_`, and referenced in flows with `{{ secret('...') }}`. Do not put raw secrets directly in `.env` — only the encoded `SECRET_*` values should live in `.env_encoded`.

Files:
- `secrets.conf`: plain-text source of truth for sensitive values (local only).
- `.env_encoded`: auto-generated base64 secrets file for Kestra (local only).
- `.env`: non-secret runtime configuration for Docker services (local only).

Steps:
1. Put all secrets used by flows in `secrets.conf` (Snowflake, Kaggle, MinIO).
2. Generate `.env_encoded`:
   - `bin/encode_secrets.sh secrets.conf .env_encoded`
3. Keep non-secret infra settings in `.env` (Postgres, Kestra basic auth, MinIO root creds). `SECRET_*` values should only be in `.env_encoded`.

Kestra reads `.env_encoded` and resolves secrets via `{{ secret('KEY') }}` without the `SECRET_` prefix.

## Local Data Lake (MinIO)
This project includes a local, S3-compatible data lake using MinIO. Raw CSVs are copied to the bucket as an additional landing zone before loading into Snowflake.

Required environment variables (plain text in `.env` and mirrored as `SECRET_` for Kestra):
- `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`
- `MINIO_BUCKET` (e.g., `olist-lake`)
- `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` (can match root user/pass)
- `MINIO_REGION` (e.g., `us-east-1`)
- `MINIO_ENDPOINT` (e.g., `http://minio:9000`)

Access MinIO console at `http://localhost:9001`.

## dbt Tracks
Two dbt tracks are available:
- **Snowflake track:** `dbt/` (warehouse-native transformations; used by the Kestra flow when `use_dbt=true`).
- **DuckDB track:** `dbt_duckdb/` (local analytics from CSVs; useful for Power BI and offline work).

The Snowflake track runs inside the pipeline when `use_dbt=true` and uses the mounted project at `/app/dbt`.

To disable dbt and run the in-warehouse SQL transforms instead, set `use_dbt=false` when executing the flow.

## Optional Data Lake Copy
The MinIO data lake copy step is optional and disabled by default to keep pipeline runs reliable.
Enable it by setting `use_lake=true` when running the `olist_pipeline` flow.

## Quickstart
1. Create `secrets.conf` with your Snowflake and Kaggle credentials.
2. Generate `.env_encoded`:
   - `bin/encode_secrets.sh secrets.conf .env_encoded`
3. Populate `.env` with non-secret values only:
   - `POSTGRES_*` and `KESTRA_BASIC_AUTH_*` values (plain text)
   - MinIO non-secret settings (see "Local Data Lake")
4. Build and start the stack: `make up`
5. Open the Kestra UI at `http://localhost:8080`.
6. Import flows (one time or after changes): `bin/import_flows.sh`
7. Run the `olist_pipeline` flow (dbt is enabled by default).

## Validation
Run these in Snowflake to confirm successful loads and transformations:

```sql
USE ROLE KESTRAINGESTION;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE KESTRA_DB;
USE SCHEMA PUBLIC;

SELECT COUNT(*) FROM olist_orders;
SELECT COUNT(*) FROM olist_customers;
SELECT COUNT(*) FROM fact_sales;
```

## Warehouse Optimization
`fact_sales` is clustered by `purchase_at` to improve time-series queries such as monthly revenue trends. This supports the dashboard and reporting use cases focused on temporal analysis.

## Dashboard
Two options are provided:
- Streamlit dashboard in `dashboard/streamlit_app.py`
- Power BI guide in `dashboard/powerbi/README.md` (uses dbt model `powerbi_dataset`)

Both cover:
- Revenue by payment type (categorical distribution)
- Monthly revenue trend (time series)

Power BI can use Snowflake (dbt) or DuckDB (local) as the data source; see `dashboard/powerbi/README.md`.

Run the Streamlit dashboard locally:
```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/streamlit_app.py
```

## Project Impact
By centralizing fragmented Kaggle CSVs into a structured Snowflake warehouse, this project reduces time-to-insight for retail stakeholders and enables consistent, repeatable revenue and delivery-performance analysis.

## Notes
- The Kaggle CLI is installed in the Kestra container via the `Dockerfile`.
- Secrets are supplied as base64-encoded `SECRET_*` environment variables and resolved via `secret('...')`.
- The pipeline is fully operational and can be extended with additional models and quality checks.
