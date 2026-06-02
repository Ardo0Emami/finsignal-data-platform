# RAW_MARKET_PRICES Contract

`FINSIGNAL_DW.RAW.RAW_MARKET_PRICES` stores source-shaped daily market price records after they have been loaded from FinSignal raw files into Snowflake.

This table is part of the raw warehouse layer. It preserves lineage back to the raw file and ingestion run.

## Grain

One row represents:

    one provider
    one dataset
    one symbol
    one price timestamp
    one ingestion run

This means the same `symbol` and `price_timestamp` may appear more than once if the data was re-ingested in separate runs.

Downstream dbt models decide which record is current or valid for analytics.

## Table

    FINSIGNAL_DW.RAW.RAW_MARKET_PRICES

## Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `provider_name` | STRING | yes | Source provider name, such as `static_sample`. |
| `dataset_name` | STRING | yes | Dataset identifier, currently `daily_prices`. |
| `symbol` | STRING | yes | Tracked asset symbol, such as `BTCUSD` or `QQQ`. |
| `price_timestamp` | TIMESTAMP_NTZ | yes | Timestamp of the source price observation. |
| `open_price` | FLOAT | no | Opening price when available. |
| `high_price` | FLOAT | no | Highest price during the observation window when available. |
| `low_price` | FLOAT | no | Lowest price during the observation window when available. |
| `close_price` | FLOAT | yes | Closing price used by downstream models. |
| `adjusted_close_price` | FLOAT | no | Adjusted closing price when available. |
| `volume` | FLOAT | no | Source volume when available. |
| `raw_path` | STRING | yes | Local or S3 raw file path that produced the row. |
| `ingestion_run_id` | STRING | yes | Ingestion run identifier matching raw metadata and audit events. |
| `ingested_at` | TIMESTAMP_NTZ | yes | Timestamp when the raw file was created. |
| `raw_record` | VARIANT | yes | Original source-shaped record preserved as semi-structured data. |

## Lineage

Each row can be traced back through:

    RAW_MARKET_PRICES.ingestion_run_id
    RAW_MARKET_PRICES.raw_path
    AUDIT.INGESTION_RUNS.run_id
    raw metadata.json

## Duplicate Handling

This raw table is append-only.

It does not enforce uniqueness on:

    symbol
    price_timestamp

That deduplication belongs in the staging layer, where dbt can apply deterministic rules such as:

    latest ingested_at per provider/symbol/price_timestamp
    successful audit runs only
    preferred provider priority

## Downstream Usage

Expected downstream layers:

| Layer | Responsibility |
|---|---|
| `RAW` | Preserve source-shaped records and lineage. |
| `STAGING` | Clean names, cast types, deduplicate, enforce basic tests. |
| `INTERMEDIATE` | Calculate return, volatility, moving averages, and regime features. |
| `MARTS` | Expose analytics-ready regime and signal tables. |
