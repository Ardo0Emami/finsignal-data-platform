# FinSignal Platform Architecture

FinSignal is a market-intelligence data platform that turns raw asset price data into governed signals, regimes, backtest outcomes, and product-facing explanations.

The platform is organized as layered data architecture rather than a single monolithic script.


## Architecture diagram

A Mermaid-based platform flow diagram is available at:

    docs/architecture/platform_flow_diagram.md

## High-level flow

    Market data providers
        |
        v
    Batch ingestion services
        |
        v
    Raw partitioned storage
        |
        v
    Snowflake RAW / AUDIT
        |
        v
    dbt STAGING / INTERMEDIATE / MARTS
        |
        v
    Product API and governed explanations

## Ingestion layer

The ingestion layer is responsible for collecting market data and writing raw records with metadata.

Responsibilities:

- provider selection
- asset universe handling
- raw file writing
- ingestion run metadata
- failure audit events
- local and S3-compatible writer contracts

The raw layout preserves lineage through fields such as:

- provider
- dataset
- symbol
- ingestion date
- run id
- raw path

## Orchestration layer

Airflow DAGs schedule ingestion workflows.

Airflow is intentionally thin. DAGs define:

- schedule
- retries
- task wiring
- operational entry points

Business logic stays in reusable Python services rather than inside DAG files.

## Raw warehouse layer

Snowflake stores raw and audit data in separate schemas.

Core schemas:

- `RAW`
- `AUDIT`

Core raw tables:

- `RAW.RAW_MARKET_PRICES`
- `RAW.RAW_PRICE_EVENTS`

Core audit tables:

- `AUDIT.INGESTION_RUNS`
- `AUDIT.DATA_QUALITY_RESULTS`

The raw layer is append-oriented and preserves lineage back to raw files.

## dbt modeling layer

dbt transforms raw data into governed analytical models.

Schemas:

- `STAGING`
- `INTERMEDIATE`
- `MARTS`

Layer responsibilities:

- `STAGING`: typed and cleaned source-aligned views
- `INTERMEDIATE`: reusable feature and classification models
- `MARTS`: product-ready facts, snapshots, signals, regimes, and backtest results

Important marts:

- `MARTS.MART_CURRENT_ASSET_SNAPSHOT`
- `MARTS.MART_ASSET_SIGNAL`
- `MARTS.MART_ASSET_REGIME`
- `MARTS.FACT_SIGNAL_DAILY`
- `MARTS.FACT_BACKTEST_RESULT`

## Event ingestion layer

The event-ingestion layer is implemented for latest-price events.

Components:

- Lambda latest-price ingestion handler
- Kinesis price-event producer and consumer contracts
- S3 event landing writer
- Snowflake raw price-event loader
- Terraform modules for Kinesis, Lambda, and IAM wiring

The infrastructure is deployment-ready, but the AWS apply step is intentionally kept separate to control cloud cost.

## PySpark feature layer

PySpark is used for file-oriented feature processing over Parquet data.

Responsibilities:

- export staged market prices to Parquet
- build asset-level feature output
- support scalable feature computation outside the warehouse path

The local implementation includes a Windows-safe fallback for writing Parquet output.

## Product API layer

FastAPI exposes modeled asset intelligence from Snowflake marts.

Core endpoints:

- `GET /health`
- `GET /api/v1/assets/{symbol}/snapshot`
- `GET /api/v1/assets/{symbol}/regime`
- `GET /api/v1/assets/{symbol}/signals`
- `POST /api/v1/ask`

The `/api/v1/ask` endpoint is governed and evidence-based. It builds answers from modeled mart outputs rather than generating unsupported free-form responses.

## Design principles

FinSignal follows these design principles:

- raw data is preserved before transformation
- lineage is carried through `ingestion_run_id` and `raw_path`
- orchestration stays thin
- transformations are tested
- product APIs read from governed marts
- cloud-cost-generating steps are explicit
- implementation boundaries are contract-tested
