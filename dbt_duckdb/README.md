# dbt (DuckDB)

This is a parallel dbt project that builds a Power BI-ready dataset locally using DuckDB and the CSVs in `data/landing`.

## Why this exists
- Keeps the Snowflake dbt project intact.
- Provides a local, recruiter-friendly analytics model for Power BI.

## Prereqs
- Python + dbt-duckdb installed.
- Local CSVs available in `data/landing`.

## Run
```bash
cd dbt_duckdb
DBT_PROFILES_DIR=. dbt run --select powerbi_dataset
```

## Configure paths
- Default DuckDB file: `../data/warehouse/olist.duckdb`
- Override with `DUCKDB_PATH` env var.
- CSV path defaults to `../data/landing` and can be overridden with `--vars '{"data_path": "../data/landing"}'`.
