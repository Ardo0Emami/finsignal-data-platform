# Reviewer Validation Checklist

This checklist gives reviewers a practical path for validating the FinSignal Data Platform.

The commands are grouped by safety level. Local checks are safe by default. Snowflake and AWS-related checks require environment configuration and may create usage cost.

## Safe local checks

Run Python linting:

    python -m ruff check .

Run the full unit test suite:

    python -m pytest

Run only API tests:

    python -m pytest tests/unit/api

Run documentation contract tests:

    python -m pytest tests/unit/docs

## dbt checks

Compile dbt models without executing warehouse transformations:

    dbt compile --project-dir dbt --profiles-dir dbt

Run dbt models against Snowflake:

    dbt run --project-dir dbt --profiles-dir dbt

Run dbt tests against Snowflake:

    dbt test --project-dir dbt --profiles-dir dbt

Snowflake-backed dbt commands require environment variables such as:

- `FINSIGNAL_SNOWFLAKE_ACCOUNT`
- `FINSIGNAL_SNOWFLAKE_USER`
- `FINSIGNAL_SNOWFLAKE_PASSWORD`
- `FINSIGNAL_SNOWFLAKE_ROLE`
- `FINSIGNAL_SNOWFLAKE_WAREHOUSE`
- `FINSIGNAL_SNOWFLAKE_DATABASE`

For local Git Bash usage:

    set -a
    source .env
    set +a

## Product API smoke test

Start the API:

    uvicorn app.main:app --reload --port 8000

Health endpoint:

    curl http://127.0.0.1:8000/health

Snapshot endpoint:

    curl http://127.0.0.1:8000/api/v1/assets/QQQ/snapshot

Regime endpoint:

    curl http://127.0.0.1:8000/api/v1/assets/QQQ/regime

Signal endpoint:

    curl http://127.0.0.1:8000/api/v1/assets/QQQ/signals

Governed explanation endpoint:

    curl -X POST http://127.0.0.1:8000/api/v1/ask \
      -H "Content-Type: application/json" \
      -d '{"symbol":"QQQ","question":"Why is QQQ buy_watch?"}'

## PySpark local feature check

Export staged market prices to Parquet:

    python -m spark.jobs.export_market_prices_to_parquet

Build asset feature output:

    python -m spark.jobs.build_asset_feature_parquet

Generated local outputs should remain uncommitted.

## AWS event-ingestion boundary

The event-ingestion layer includes Terraform modules and implementation code for:

- Lambda latest-price ingestion
- Kinesis price-event stream
- Kinesis consumer
- S3 event landing
- Snowflake raw event loading

Do not run the following unless intentionally activating AWS resources:

    terraform apply

Use `terraform plan` first and review expected resources and cost implications.

## Expected reviewer path

A typical safe reviewer path is:

1. Read `docs/positioning/reviewer_summary.md`.
2. Read `docs/positioning/project_status.md`.
3. Read `docs/architecture/platform_flow_diagram.md`.
4. Run `python -m ruff check .`.
5. Run `python -m pytest`.
6. Optionally run dbt/API smoke tests if Snowflake environment variables are available.
