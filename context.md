# Project Objective: Kestra-Snowflake Olist Data Pipeline

## Goal
Build a production-grade workflow orchestration pipeline that downloads the Brazilian e-commerce dataset from Kaggle and loads it into Snowflake using Kestra.

## Constraints
- **Security**: No hardcoded secrets, use environment variables or Kestra secrets
- **Modularity**: Separate flows for extraction, loading, and transformation
- **Idempotency**: Flows can run multiple times without duplicating data
- **Observability**: Clear logging and error handling at each step

## Requirements

### Data Source
| Source | Dataset | Contents |
|--------|---------|----------|
| Kaggle | `olistbr/brazilian-ecommerce` | 9 CSV files: customers, geolocation, items, payments, reviews, orders, products, sellers, category translation |

### Infrastructure
| Component | Technology | Role |
|-----------|-----------|------|
| Orchestrator | Kestra (Docker) | Workflow scheduling and execution |
| Database | Snowflake | Data warehouse for storage/transformation |
| Credentials | `.env` file (gitignored) | Environment variable injection |

### Flow Architecture
Flow 1: olist_download (Kaggle -> Local CSVs)
↓
Flow 2: snowflake_loader (CSVs -> Snowflake staging tables)
↓
Flow 3: snowflake_transform (Staging -> Analytics views/joins)
