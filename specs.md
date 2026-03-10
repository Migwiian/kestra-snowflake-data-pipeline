# PRD: Kestra Snowflake Olist Pipeline Upgrades

## Goal
Incrementally upgrade the existing Kestra → Snowflake pipeline to meet Data Engineering Zoomcamp project requirements without destabilizing the current working flow. Changes should be additive, minimal-risk, and gated where possible.

## Non-Goals
- Rewriting the existing pipeline logic.
- Replacing Snowflake with another warehouse.
- Introducing breaking changes to current flows.

## Current Baseline
- End-to-end Kestra orchestration works: download → load → transform.
- Snowflake staging tables and simple analytical tables are created.
- Docker Compose local stack is functional.

## Upgrade Phases (Ordered)

### Phase 1: Problem Statement + Success Criteria (docs only, zero runtime risk)
- Add a short “Problem Statement” section to `README.md`.
- Add “Success Metrics” section with 2–3 KPIs.
- No pipeline changes.
Status: Implemented (added Problem Statement + Success Metrics to `README.md`).

### Phase 2: Data Lake Landing (minimal pipeline change, add-only)
- Add a flow to copy downloaded CSVs from Kestra internal storage to a cloud data lake (S3/GCS/ADLS).
- Keep the existing Snowflake load path intact; data lake is an additional sink.
- Insert the new flow between download and load in `flows/olist_pipeline.yml`.
- Document lake location and file layout in `README.md`.
Status: Implemented (MinIO local lake + `olist_lake` flow wired into pipeline).

### Phase 3: IaC Skeleton (no impact to runtime pipeline)
- Add minimal Terraform or Pulumi module to provision the data lake bucket and (optionally) a Snowflake external stage.
- Keep IaC optional and documented in `README.md`.
- No flow changes required.
Status: Implemented (Terraform skeleton in `infra/terraform/`).

### Phase 4: Warehouse Optimization (small SQL change, low risk)
- Add clustering/partitioning guidance for Snowflake tables (e.g., `CLUSTER BY (purchase_at)` on `fact_sales`).
- Implement as `ALTER TABLE` or clustered table creation in `flows/snowflake_transform.yml`.
- Add a short rationale in `README.md`.
Status: Implemented (clustered `fact_sales` by `purchase_at`).

### Phase 5: Transformations Depth (add dbt without breaking existing SQL)
- Keep current SQL transforms as default.
- Add an optional `dbt/` project that reproduces `olist_orders_cleaned` and `fact_sales`.
- Add a new Kestra task behind a feature-flag input (default off).
- Document how to toggle.
Status: Implemented (optional dbt project and `use_dbt` flag).

### Phase 6: Dashboard Deliverable (BI only, no pipeline risk)
- Create a BI dashboard with at least two tiles:
  - Categorical distribution (e.g., revenue by payment type).
  - Temporal trend (e.g., monthly revenue or orders).
- Add a screenshot to `docs/` and link it from `README.md`.

## Delivery Principles
- Additive changes first.
- Feature-flag optional components.
- Avoid touching working ingestion unless necessary.
- Every phase should be independently shippable.

## Success Criteria
- Project meets Zoomcamp rubric requirements.
- Current pipeline remains functional at every phase.
- Clear documentation of how to run optional components.

## Current Status / Blockers
- Kestra runs with Postgres repository and flows import correctly.
- `snowflake_transform` with `use_dbt=true` fails because secrets are not found in Kestra runtime.
- Root cause: the Kestra container is not loading `.env_encoded`, so `SECRET_*` variables are missing.
- Fix required:
  1. Ensure `docker-compose.yml` includes `.env_encoded` under `kestra.env_file`.
  2. Recreate the Kestra container.
  3. Verify `SECRET_*` variables exist inside the container.
  4. Re-run `snowflake_transform` with `use_dbt=true`.
