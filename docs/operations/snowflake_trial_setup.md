# Snowflake Trial Setup Runbook

This runbook explains how to connect FinSignal to a Snowflake trial account safely.

## When to Use This

Use this after local raw ingestion, Airflow orchestration, and Snowflake loader tests are passing.

Do not use real Snowflake credentials until the local loader and schema tests pass.

## Trial Notes

Snowflake trial accounts are suitable for validating the FinSignal raw-load workflow.

The project uses a cost-controlled development warehouse:

    FINSIGNAL_DEV_WH

with:

    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE

## Required Environment Variables

Set these values in `.env`:

    FINSIGNAL_SNOWFLAKE_ACCOUNT=
    FINSIGNAL_SNOWFLAKE_USER=
    FINSIGNAL_SNOWFLAKE_PASSWORD=
    FINSIGNAL_SNOWFLAKE_ROLE=
    FINSIGNAL_SNOWFLAKE_WAREHOUSE=FINSIGNAL_DEV_WH
    FINSIGNAL_SNOWFLAKE_DATABASE=FINSIGNAL_DW
    FINSIGNAL_SNOWFLAKE_SCHEMA=RAW

Do not commit `.env`.

## Validation Order

Run these commands in order:

    python -m scripts.snowflake.check_snowflake_ready
    python -m scripts.snowflake.test_connection
    python -m scripts.snowflake.apply_schema
    python -m scripts.snowflake.load_raw_market_prices --limit 2

## Manual Verification Queries

After loading data, verify rows:

    SELECT
        provider_name,
        dataset_name,
        symbol,
        COUNT(*) AS row_count,
        MIN(price_timestamp) AS min_price_timestamp,
        MAX(price_timestamp) AS max_price_timestamp
    FROM FINSIGNAL_DW.RAW.RAW_MARKET_PRICES
    GROUP BY 1, 2, 3
    ORDER BY symbol;

Verify ingestion lineage:

    SELECT
        ingestion_run_id,
        symbol,
        raw_path,
        COUNT(*) AS row_count
    FROM FINSIGNAL_DW.RAW.RAW_MARKET_PRICES
    GROUP BY 1, 2, 3
    ORDER BY symbol, ingestion_run_id;

## Cost Safety

After testing, suspend the warehouse:

    ALTER WAREHOUSE FINSIGNAL_DEV_WH SUSPEND;

Only use small test loads first:

    python -m scripts.snowflake.load_raw_market_prices --limit 2

Do not run broad historical loads until the dbt staging layer exists.
