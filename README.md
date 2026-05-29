# FinSignal Data Platform

FinSignal is a market intelligence data platform for regime detection, signal validation, backtesting, and explainable financial analytics.

It ingests market and macro data from external sources, lands raw source-shaped data in an append-only raw zone, models analytical datasets for market regimes and signals, validates signal outcomes through backtesting, and exposes governed explanations through a product API.

FinSignal does not provide investment advice, trading recommendations, or guaranteed predictions. It is an analytical decision-support platform designed around explainable, testable market intelligence.

## Current Implementation Status

The current foundation includes:

- Python project structure
- FastAPI application foundation with health endpoint
- Static market data provider
- Normalized market price record model
- Local raw landing writer
- Partitioned raw data output
- Raw metadata generation with checksum
- Reusable local ingestion script
- Unit tests for provider and writer behavior
- GitHub Actions workflow for Python validation

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

Run the local ingestion flow:

    python -m scripts.ingestion.run_market_ingestion

Run the API locally:

    python -m uvicorn app.main:app --reload

Health check:

    curl http://127.0.0.1:8000/health

## Runtime Configuration

FinSignal uses environment variables for runtime configuration.

The local template is provided in `.env.example`.

Supported raw writer modes:

    FINSIGNAL_RAW_WRITER=local

This writes raw files under the local `data/` directory.

    FINSIGNAL_RAW_WRITER=s3
    FINSIGNAL_RAW_BUCKET=finsignal-dev-raw

This writes raw files to AWS S3.

The same ingestion entry point is used for both modes:

    python -m scripts.ingestion.run_market_ingestion

## Raw Landing Contract

Local raw files are written using a partitioned structure that mirrors the future S3 raw landing zone:

    data/raw/provider=<provider>/dataset=<dataset>/symbol=<symbol>/ingestion_date=<date>/run_id=<uuid>/data.json
    data/raw/provider=<provider>/dataset=<dataset>/symbol=<symbol>/ingestion_date=<date>/run_id=<uuid>/metadata.json

Raw outputs are append-only. Each run receives a unique run_id.

Metadata includes:

- provider
- dataset
- symbol
- record count
- ingestion timestamp
- schema version
- SHA-256 checksum
- data path

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
