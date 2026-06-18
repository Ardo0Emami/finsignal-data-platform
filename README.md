# FinSignal Data Platform

FinSignal is a market intelligence data platform for regime detection, signal validation, backtesting, and explainable financial analytics.

It ingests market and macro data from external sources, lands raw source-shaped data in an append-only raw zone, models analytical datasets for market regimes and signals, validates signal outcomes through backtesting, and exposes governed explanations through a product API.

FinSignal does not provide investment advice, trading recommendations, or guaranteed predictions. It is an analytical decision-support platform designed around explainable, testable market intelligence.

## Current Implementation Status

FinSignal currently includes a working local-first data engineering foundation with batch ingestion, Snowflake raw loading, dbt analytics modeling, testing, and infrastructure-as-code foundations.

Implemented components include:

- Python project structure with FastAPI health endpoint
- configurable market data provider layer
- static sample provider for BTCUSD and QQQ daily prices
- normalized market price record model
- local raw writer with partitioned raw output paths
- S3 raw writer abstraction for cloud raw landing
- ingestion service orchestration with success and failure audit events
- local audit writer for ingestion metadata
- reusable ingestion entrypoints and inspection scripts
- Airflow DAG foundation for scheduled market ingestion
- Snowflake schema scripts for warehouse, database, RAW, and AUDIT objects
- Snowflake raw load flow using local NDJSON files, internal stages, PUT, and COPY INTO
- Snowflake verification queries for loaded raw market price data
- dbt project foundation
- dbt source definitions for Snowflake RAW tables
- dbt staging models for normalized and deduplicated market price records
- dbt intermediate models for analytical transformations, returns, technical features, and signal classification logic
- dbt marts for analytics-ready market datasets, current asset snapshots, regimes, and signals
- dbt fact models for historical signal outputs and backtest results
- dbt tests for key data quality assumptions, accepted values, and unique model grain
- dbt documentation and lineage generation support
- streaming/event ingestion foundation with PriceEvent contracts, Kinesis producer abstraction, Kinesis-to-S3 consumer abstraction, and S3 event writer
- Terraform storage, IAM, Kinesis, and Lambda ingestion module foundations
- PySpark feature processing foundation for staged Parquet market data
- unit tests for ingestion, Snowflake loading, dbt contracts, streaming abstractions, and Terraform module contracts
- GitHub Actions CI for Python linting and tests


## Local Development

Create virtual environment:

    python -m venv .venv

Activate virtual environment on Git Bash for Windows:

    source .venv/Scripts/activate

Install dependencies:

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

Run validation:

    python -m ruff check .
    python -m pytest

Run the market ingestion flow:

    python -m scripts.ingestion.run_market_ingestion

Run the API locally:

    python -m uvicorn app.main:app --reload

Health check:

    curl http://127.0.0.1:8000/health

## Runtime Configuration

FinSignal uses environment variables for runtime configuration.

The local template is provided in `.env.example`.

Market data provider:

    FINSIGNAL_MARKET_DATA_PROVIDER=static_sample

Asset universe:

    FINSIGNAL_ASSET_SYMBOLS=BTCUSD,QQQ

Local raw writer mode:

    FINSIGNAL_RAW_WRITER=local

This writes raw files under the local `data/` directory.

S3 raw writer mode:

    FINSIGNAL_RAW_WRITER=s3
    FINSIGNAL_RAW_BUCKET=finsignal-dev-raw

This writes raw files to AWS S3.

The same ingestion entry point is used for both modes:

    python -m scripts.ingestion.run_market_ingestion

Inspect recent local ingestion audit events:

    python -m scripts.audit.inspect_ingestion_audit

## Raw Landing Contract

Local raw files are written using a partitioned structure that mirrors the future S3 raw landing zone:

    data/raw/provider=<provider>/dataset=<dataset>/symbol=<symbol>/ingestion_date=<date>/run_id=<uuid>/data.json
    data/raw/provider=<provider>/dataset=<dataset>/symbol=<symbol>/ingestion_date=<date>/run_id=<uuid>/metadata.json

S3 raw files use the same logical layout:

    s3://<bucket>/raw/provider=<provider>/dataset=<dataset>/symbol=<symbol>/ingestion_date=<date>/run_id=<uuid>/data.json
    s3://<bucket>/raw/provider=<provider>/dataset=<dataset>/symbol=<symbol>/ingestion_date=<date>/run_id=<uuid>/metadata.json

Raw outputs are append-only. Each run receives a unique `run_id`.

Metadata includes:

- provider
- dataset
- symbol
- record count
- ingestion timestamp
- schema version
- SHA-256 checksum
- data path

## Ingestion Audit Contract

FinSignal writes ingestion audit events for each symbol-level ingestion run.

Local audit events are written under:

    data/audit/ingestion_events/dataset=<dataset>/symbol=<symbol>/<run_id>.json

Each audit event includes:

- run_id
- provider_name
- dataset_name
- symbol
- status
- started_at
- completed_at
- records_extracted
- records_written
- raw_path
- error_message

The audit `run_id` matches the raw output `run_id`, so every raw file can be traced back to the ingestion event that produced it.

Successful ingestion events use:

    status=succeeded

Failed ingestion events use:

    status=failed

Failure audit events preserve the error message so ingestion failures remain traceable instead of disappearing as unstructured exceptions.

## Airflow Orchestration

FinSignal uses Airflow for scheduled workflow orchestration.

Airflow DAGs must stay thin. They define schedules, retries, and task wiring, then call reusable project entry points.

The daily market ingestion DAG calls:

    scripts.ingestion.run_market_ingestion.run_full_pipeline

This keeps ingestion business logic outside Airflow and inside the reusable ingestion service layer.

Airflow is intentionally not installed in the base local Python environment. It should run in a dedicated Airflow runtime/container because Airflow has its own dependency constraints.

Current DAG location:

    airflow/dags/market_daily_ingestion_dag.py

The DAG currently orchestrates the same ingestion flow that can be run locally with:

    python -m scripts.ingestion.run_market_ingestion

## Local Airflow Runtime

Airflow is used for local scheduled orchestration during development.

Start Airflow:

    cd airflow
    docker compose up airflow-init
    docker compose up -d

Open Airflow UI:

    http://localhost:8080

Default local credentials:

    username: airflow
    password: airflow

List running containers:

    docker compose ps

View scheduler logs:

    docker compose logs -f airflow-scheduler

Stop Airflow:

    docker compose down

Stop Airflow and remove local metadata volume:

    docker compose down -v

The local Airflow runtime mounts the project source code into the Airflow containers and uses the same ingestion entry point as local execution:

    scripts.ingestion.run_market_ingestion.run_full_pipeline


## Snowflake Cost Guardrails

FinSignal uses a dedicated development warehouse for Snowflake testing:

    FINSIGNAL_DEV_WH

The warehouse is configured as:

    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE

For local testing:

1. Use the smallest warehouse.
2. Run only small loads first.
3. Verify results with targeted queries.
4. Suspend the warehouse after testing.

Manual suspend command:

    ALTER WAREHOUSE FINSIGNAL_DEV_WH SUSPEND;

Do not use always-on warehouses for this project.


## Snowflake Connection Test

Before applying schemas or loading data, validate that Snowflake credentials are configured:

    python -m scripts.snowflake.check_snowflake_ready

Then test the actual Snowflake connection:

    python -m scripts.snowflake.test_connection

The connection test prints the active account, user, role, warehouse, database, and schema.


## Snowflake Raw Load

Phase 3 introduces the Snowflake raw-load foundation.

Create Snowflake database and schemas:

    python -m scripts.snowflake.apply_schema

Inspect latest local raw market price files as warehouse-ready rows:

    python -m scripts.snowflake.inspect_raw_market_price_rows --limit 5

Load latest local raw market price files into Snowflake:

    python -m scripts.snowflake.load_raw_market_prices --limit 5

Snowflake connection settings are configured through environment variables:

    FINSIGNAL_SNOWFLAKE_ACCOUNT=
    FINSIGNAL_SNOWFLAKE_USER=
    FINSIGNAL_SNOWFLAKE_PASSWORD=
    FINSIGNAL_SNOWFLAKE_ROLE=
    FINSIGNAL_SNOWFLAKE_WAREHOUSE=
    FINSIGNAL_SNOWFLAKE_DATABASE=FINSIGNAL_DW
    FINSIGNAL_SNOWFLAKE_SCHEMA=RAW

The Snowflake raw market price table is:

    FINSIGNAL_DW.RAW.RAW_MARKET_PRICES

The Snowflake ingestion audit table is:

    FINSIGNAL_DW.AUDIT.INGESTION_RUNS

The raw-loader path is intentionally separated into two steps:

1. Convert local raw files into warehouse-ready rows.
2. Load those rows into Snowflake.

This keeps parsing, validation, and warehouse writes independently testable.

## dbt Analytics Modeling

FinSignal uses dbt to transform Snowflake raw market data into tested, documented, analytics-ready models.

The dbt layer includes:

- source definitions for Snowflake RAW tables
- staging models for normalized and deduplicated market price records
- intermediate models for reusable analytical transformations, including returns, technical features, and centralized signal classifications
- mart models for downstream analytics, current asset snapshots, explainable regimes, signal validation, and backtesting
- fact models for historical daily signal outputs and forward-return backtest results
- data tests for key assumptions, accepted values, required fields, and model grain uniqueness
- documentation and lineage support through dbt model and source definitions

This layer separates raw source-preserved data from cleaned, modeled, and analytics-ready datasets. It also keeps signal logic centralized so current signal views, historical signal facts, and backtest models are derived from the same tested transformation layer.


## PySpark Feature Processing

FinSignal uses PySpark for file-based feature processing over staged Parquet datasets.

Spark does not replace Snowflake or dbt in this project. Snowflake remains the analytical warehouse, and dbt remains the warehouse transformation, testing, and documentation layer.

The Spark layer is used when feature processing should operate over files, especially Parquet datasets, and when larger historical windows may become expensive or inconvenient to process only inside the warehouse.

Current Spark jobs include:

- `spark/jobs/export_market_prices_to_parquet.py`
- `spark/jobs/build_asset_feature_parquet.py`

The local Spark flow is:

    local raw market price JSON
      -> staged market price Parquet
      -> PySpark feature job
      -> asset feature Parquet output

Export local raw market price files to staged Parquet:

    python -m spark.jobs.export_market_prices_to_parquet \
      --raw-root data/raw \
      --output data/staged/market_prices

Run the PySpark feature job:

    python -m spark.jobs.build_asset_feature_parquet \
      --input data/staged/market_prices \
      --output data/features/asset_features

Inspect generated feature files:

    find data/features/asset_features -maxdepth 2 -type f | sort

Default staged input path:

    data/staged/market_prices

Default feature output path:

    data/features/asset_features

Generated feature columns include:

- previous_close_price
- daily_return
- close_price_3d_moving_avg
- daily_return_3d_volatility
- close_vs_3d_moving_avg

Feature processing preserves lineage fields such as:

- raw_path
- ingestion_run_id
- ingested_at

This allows downstream warehouse or API layers to trace feature rows back to the raw ingestion process.

In local development, Spark runs with:

    local[*]

This means the job runs locally and does not create cloud compute cost.

A managed Spark service such as AWS Glue, EMR, or Databricks should only be introduced when local execution no longer fits the data volume or orchestration requirements.

FinSignal uses PySpark for file-based feature processing over staged Parquet market data. This complements the Snowflake/dbt warehouse modeling layer and demonstrates that large-window or file-oriented feature generation can be separated from warehouse transformation logic when appropriate.

## Architecture Direction

FinSignal is being built as a product-style data platform with clear responsibilities across:

- AWS and Terraform for reproducible infrastructure
- S3 for raw data lake storage
- Lambda and Kinesis for event-style ingestion
- Airflow for scheduled orchestration
- Snowflake for analytical warehouse storage
- dbt for modular warehouse transformations
- PySpark for file-based feature processing
- FastAPI for product API access
- GitHub Actions for validation
- Data quality, audit tables, and observability for operational trust
- Backtesting and signal versioning for analytical correctness
