import os

import pandas as pd
import snowflake.connector
import streamlit as st


def _get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


@st.cache_data(ttl=300)
def _run_query(sql: str) -> pd.DataFrame:
    with _get_connection() as conn:
        return pd.read_sql(sql, conn)


st.set_page_config(page_title="Olist Revenue Dashboard", layout="wide")

st.title("Olist Revenue Dashboard")
st.caption("Kestra → Snowflake → dbt")

metric_sql = """
SELECT
  COUNT(DISTINCT order_id) AS total_orders,
  SUM(total_order_value)   AS total_revenue
FROM fact_sales;
"""

payment_sql = """
SELECT
  payment_type,
  SUM(total_order_value) AS total_revenue
FROM fact_sales
GROUP BY 1
ORDER BY total_revenue DESC;
"""

monthly_sql = """
SELECT
  DATE_TRUNC('month', purchase_at) AS month,
  SUM(total_order_value)           AS total_revenue
FROM fact_sales
GROUP BY 1
ORDER BY 1;
"""

try:
    metrics = _run_query(metric_sql)
    payments = _run_query(payment_sql)
    monthly = _run_query(monthly_sql)

    col1, col2 = st.columns(2)
    col1.metric("Total Orders", f"{int(metrics.iloc[0]['TOTAL_ORDERS']):,}")
    col2.metric("Total Revenue", f"${metrics.iloc[0]['TOTAL_REVENUE']:,.2f}")

    left, right = st.columns(2)
    left.subheader("Revenue by Payment Type")
    left.bar_chart(
        payments.set_index("PAYMENT_TYPE")["TOTAL_REVENUE"],
        height=350,
    )

    right.subheader("Monthly Revenue")
    monthly_plot = monthly.rename(columns={"MONTH": "month", "TOTAL_REVENUE": "total_revenue"})
    right.line_chart(
        monthly_plot.set_index("month")["total_revenue"],
        height=350,
    )
except KeyError:
    st.error("Missing Snowflake env vars. Set SNOWFLAKE_* before running.")
except Exception as exc:
    st.error(f"Dashboard query failed: {exc}")
