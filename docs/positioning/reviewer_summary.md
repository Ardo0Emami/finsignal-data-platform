# FinSignal Reviewer Summary

FinSignal is a market-intelligence data platform that demonstrates end-to-end data engineering across ingestion, orchestration, warehouse modeling, feature processing, signal generation, backtesting, and product API delivery.

It is designed as a realistic platform project rather than a notebook-only analytics exercise.

## What the platform does

FinSignal ingests asset price data, preserves raw records, loads them into Snowflake, transforms them with dbt, generates explainable signal and regime outputs, computes historical backtest outcomes, and exposes the resulting intelligence through a FastAPI product layer.

A reviewer can inspect the platform from multiple angles:

- raw ingestion and auditability
- Snowflake raw and audit tables
- dbt staging, intermediate, and mart models
- PySpark feature processing over Parquet
- event-ingestion implementation boundaries
- product API endpoints over governed marts
- evidence-based `/api/v1/ask` explanations

## Core platform capabilities

### Batch ingestion

The project includes reusable ingestion services, provider contracts, local and S3-compatible writers, ingestion metadata, and Airflow DAGs.

### Warehouse loading

Raw market data is loaded into Snowflake with lineage fields such as `ingestion_run_id` and `raw_path`.

### dbt modeling

dbt builds governed analytical layers:

- `STAGING`
- `INTERMEDIATE`
- `MARTS`

The marts expose current asset snapshots, signals, regimes, daily signal facts, and backtest outcomes.

### Event ingestion

The project includes a deployment-ready event-ingestion layer with Lambda, Kinesis, S3 landing, Snowflake raw-event loading, Terraform modules, and runbooks.

The AWS activation step is intentionally separated from implementation to avoid accidental cloud cost.

### PySpark feature processing

The platform includes PySpark jobs that export staged market prices to Parquet and generate asset-level feature output.

### Product API

FastAPI exposes product-facing endpoints over Snowflake marts:

- `GET /api/v1/assets/{symbol}/snapshot`
- `GET /api/v1/assets/{symbol}/regime`
- `GET /api/v1/assets/{symbol}/signals`
- `POST /api/v1/ask`

The `/api/v1/ask` endpoint is governed and evidence-based. It builds answers from modeled signal, regime, and snapshot evidence.

## What this project demonstrates

FinSignal demonstrates practical data engineering skills:

- Python service design
- testable ingestion architecture
- raw data preservation
- lineage and audit metadata
- Airflow orchestration
- Snowflake warehouse modeling
- dbt layered transformations
- dbt tests and contract thinking
- event-ingestion design with AWS Lambda and Kinesis
- Terraform module design
- PySpark feature processing
- FastAPI product delivery
- documentation and operational runbooks
- cost-aware cloud boundaries

## Current execution status

Implemented and locally or warehouse-validated:

- batch ingestion
- raw file writing
- Airflow DAG contracts
- Snowflake raw loading
- dbt modeling and tests
- signal and regime marts
- backtest fact mart
- PySpark feature output
- FastAPI read endpoints
- governed `/api/v1/ask` endpoint
- product API smoke tests against Snowflake

Implemented but intentionally not cloud-applied by default:

- AWS Lambda latest-price ingestion
- Kinesis price-event stream
- event consumer infrastructure
- Terraform-managed AWS event resources

## Design intent

The project prioritizes production-style boundaries:

- keep raw and modeled data separate
- keep orchestration thin
- keep transformations testable
- expose product APIs only from governed marts
- preserve lineage from API outputs back to raw records
- make cost-generating actions explicit
