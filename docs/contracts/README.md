# FinSignal Data Contracts

This directory documents the stable contracts that connect FinSignal platform layers.

A contract describes what downstream code can rely on: table purpose, grain, key fields, lineage fields, and expected behavior.

## Contract groups

### Raw contracts

Raw contracts describe source-aligned records loaded into Snowflake.

Current raw contracts:

- `raw_market_prices.md`
- `RAW.RAW_PRICE_EVENTS` is documented through the event-ingestion runbook and loader tests.

Raw contracts preserve ingestion lineage through:

- `ingestion_run_id`
- `raw_path`
- provider and dataset fields
- raw source record fields where applicable

### Audit contracts

Audit contracts describe operational metadata for ingestion and quality tracking.

Current audit contracts:

- `ingestion_runs.md`

Audit contracts help answer operational questions such as:

- which run loaded a record?
- when did ingestion start and finish?
- did the run succeed or fail?
- where did the raw file land?

### Mart contracts

Mart contracts describe product-ready analytical outputs.

Current mart contracts:

- `fact_backtest_result.md`

Important modeled marts also covered by dbt schema tests and API contracts:

- `MARTS.MART_CURRENT_ASSET_SNAPSHOT`
- `MARTS.MART_ASSET_SIGNAL`
- `MARTS.MART_ASSET_REGIME`
- `MARTS.FACT_SIGNAL_DAILY`

### API contracts

API contracts describe product-facing responses over governed marts.

Current API contracts:

- `product_api.md`

The Product API reads from `MARTS`, not directly from raw files.

## Contract principles

FinSignal contracts follow these principles:

- raw records are preserved before transformation
- modeled outputs expose stable business meaning
- lineage fields remain available to connect marts back to raw data
- dbt tests enforce important expectations
- API responses are backed by governed mart outputs
- `/api/v1/ask` returns evidence-based explanations rather than unsupported free-form answers

## How to add a new contract

When adding a new table, mart, or API endpoint:

1. Document the purpose.
2. Define the grain.
3. List required fields.
4. List lineage fields.
5. Add tests that enforce the contract.
6. Update this index.
