# Dashboards

This repo provides a Streamlit dashboard and a Power BI guide. Both visualize revenue by payment type and monthly revenue trend.

It reads from Snowflake tables created by the pipeline (`fact_sales`).

## Streamlit: Run locally
1. Export your Snowflake credentials (same values used for the pipeline): `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`.
2. Install dependencies:
   ```bash
   pip install -r dashboard/requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```

## Screenshot
After running the dashboard, capture a screenshot and store it at `docs/dashboard.svg`
or replace it with a real image (png/jpg) if preferred.

## Power BI
See `dashboard/powerbi/README.md` for data import steps, visuals, and a sample SQL query.
