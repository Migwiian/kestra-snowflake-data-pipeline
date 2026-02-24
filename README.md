# Kestra Snowflake Olist Pipeline

This project delivers an end-to-end, orchestration-first data pipeline using Kestra to ingest the Olist e-commerce dataset from Kaggle and load it into Snowflake. The primary objective is to demonstrate a production-ready data lifecycle—moving from raw, denormalized landing zones to structured analytical views within a cloud data warehouse. The repository demonstrates production-minded data engineering practices: explicit orchestration, separable staging and transformation layers, containerized execution, and predictable environment management.

## What This Pipeline Does
1. Downloads and unzips the Olist dataset via the Kaggle CLI.
2. Uploads all CSVs to Snowflake staging and loads them with the stage-and-copy pattern.
3. Builds curated analytical tables in Snowflake for downstream analysis.
4. Orchestrates the workflow as a single, repeatable pipeline.

## Architecture and Design Highlights
- Orchestration-first design with independent, composable flows.
- Clear separation between ingestion (staging tables) and transformation (analytics tables).
- Explicit Snowflake object creation, file formats, and load commands for repeatability.
- Containerized execution with a custom Kestra image that includes the Kaggle CLI.
- Secret management aligned to Kestra's `secret('...')` resolver.
- Pipeline designed for transparency and easy debugging in the Kestra UI.
- Idempotency-aware design: Snowflake load logic is structured to support schema checks and table truncation/merge strategies so repeated runs can converge on a consistent state.

## Repository Layout
- `flows/olist_download.yml`: Downloads dataset and stores files in Kestra internal storage.
- `flows/snowflake_loader.yml`: Creates Snowflake objects and loads all CSVs.
- `flows/snowflake_transform.yml`: Builds analytical tables (`olist_orders_cleaned`, `fact_sales`). This stage implements a modular transformation layer, moving data from Raw (Bronze) staging tables to Analytical (Silver/Gold) fact and dimension tables.
- `flows/olist_pipeline.yml`: Orchestrates download → load → transform.
- `docker-compose.yml`: Runs Kestra and Postgres with local storage mounts.
- `Dockerfile`: Extends `kestra/kestra` with Python and Kaggle CLI.
- `secrets.conf`: Source-of-truth credentials (plain text, local only).
- `.env`: Runtime configuration consumed by Docker/Kestra (plain text, local only).

## Environment and Secret Management
This project implements a Single Source of Truth pattern. We utilize the Kestra internal secret resolver, where environment variables prefixed with `SECRET_` are automatically mapped to the `{{ secret('...') }}` function within YAML flows.

secrets.conf: Local vault for master credentials (excluded from version control).
.env: Local runtime configuration.

This architecture ensures a clean separation between infrastructure configuration (Docker/Postgres) and sensitive service credentials (Snowflake/Kaggle), facilitating a high security posture during local development.

1. Put all Snowflake and Kaggle credentials in `secrets.conf`.
2. Mirror those values into `.env` using the same keys, prefixed with `SECRET_`.
3. Keep Postgres and Kestra UI values in `.env` as plain text.

Both `secrets.conf` and `.env` are ignored by Git and must be managed locally.

## Quickstart
1. Create `secrets.conf` with your Snowflake and Kaggle credentials.
2. Populate `.env` with:
   - `SECRET_SNOWFLAKE_*` and `SECRET_KAGGLE_*` values (plain text)
   - `POSTGRES_*` and `KESTRA_BASIC_AUTH_*` values (plain text)
3. Build and start the stack: `make up`
4. Open the Kestra UI at `http://localhost:8080`.
5. Run the `olist_pipeline` flow.

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

## Notes
- The Kaggle CLI is installed in the Kestra container via the `Dockerfile`.
- Kestra secrets are provided through environment variables prefixed with `SECRET_`.
- The pipeline is fully operational and can be extended with additional models and quality checks.
