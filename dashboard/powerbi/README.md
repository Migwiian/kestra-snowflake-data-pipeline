# Dashboard (Power BI)

This provides a Power BI alternative to the Streamlit dashboard. You can build `powerbi_dataset` in Snowflake (dbt) or locally using DuckDB (parallel dbt project).

This is intentionally designed as a portfolio artifact: you can point to dbt modeling, Power BI reporting, or both depending on the role.

## Data import (Snowflake)
1. Build the dbt model `powerbi_dataset`: `dbt run --select powerbi_dataset --profiles-dir dbt --project-dir dbt`.
2. Open Power BI Desktop.
3. Get Data -> Snowflake.
4. Provide the connection details: Server is `<SNOWFLAKE_ACCOUNT>.snowflakecomputing.com`, Warehouse is `SNOWFLAKE_WAREHOUSE`, Database is `SNOWFLAKE_DATABASE`, Schema is `SNOWFLAKE_SCHEMA`.
5. Choose `powerbi_dataset` OR use the custom SQL in `dashboard/powerbi/olist_powerbi_dataset.sql` to pre-aggregate.

## Data import (DuckDB local)
1. Build the dbt model `powerbi_dataset`: `cd dbt_duckdb && DBT_PROFILES_DIR=. dbt run --select powerbi_dataset`.
2. Export to CSV (requires DuckDB CLI): `duckdb data/warehouse/olist.duckdb \"COPY powerbi_dataset TO 'data/warehouse/powerbi_dataset.csv' (HEADER, DELIMITER ',');\"`
3. Open Power BI Desktop.
4. Get Data -> Text/CSV and select `data/warehouse/powerbi_dataset.csv`.

## Suggested visuals (minimum requirement)
- Revenue by payment type (categorical distribution).
- Monthly revenue trend (time series).

## Optional DAX measures
If you load `powerbi_dataset` directly, create these measures:

```text
Total Revenue = SUM(powerbi_dataset[payment_value_total])
Order Count = DISTINCTCOUNT(powerbi_dataset[order_id])
Avg Order Value = DIVIDE([Total Revenue], [Order Count])
```

## Screenshot
After building the report, export a screenshot to `docs/powerbi_dashboard.svg` (or `.png`) and update `README.md` if needed.
