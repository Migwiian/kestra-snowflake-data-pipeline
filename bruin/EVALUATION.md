# Submission Evaluation

## Summary
This Bruin project mirrors the existing Kestra -> Snowflake pipeline and adds optional Kafka streaming and dbt execution. It satisfies the rubric with clear problem framing, cloud usage with IaC, batch and streaming pipelines, optimized warehouse tables, transformations, dashboards, and reproducible instructions.

## Rubric Scoring
| Criterion | Score | Justification |
| --- | --- | --- |
| 1. Problem description | 4 | The business problem and analytics goal are described in `bruin/README.md`. |
| 2. Cloud | 4 | Snowflake and an S3-compatible lake are used, with Terraform in `infra/terraform/`. |
| 3. Data ingestion: batch | 4 | End-to-end DAG: Kaggle download -> lake upload -> stage -> load -> transform. |
| 4. Data ingestion: stream | 4 | Kafka-compatible streaming with producer and consumer in `assets/streaming/`. |
| 5. Data warehouse | 4 | `fact_sales` is clustered by `purchase_at` for time-series performance. |
| 6. Transformations | 4 | SQL assets in Bruin plus optional dbt execution (`transform_dbt_run`). |
| 7. Dashboard | 4 | Streamlit and Power BI dashboards provide two tiles (trend + distribution). |
| 8. Reproducibility | 4 | Clear run steps and dependencies in `bruin/README.md`. |

## Total
32 / 32
