# Product API Runbook

This runbook explains how to run and smoke-test the FinSignal Product API locally.

## Prerequisites

Install project dependencies and make sure the Snowflake environment variables are available.

Required variables include:

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

## Start the API

    uvicorn app.main:app --reload --port 8000

## Smoke tests

Health:

    curl http://127.0.0.1:8000/health

Latest asset snapshot:

    curl http://127.0.0.1:8000/api/v1/assets/QQQ/snapshot

Latest asset regime:

    curl http://127.0.0.1:8000/api/v1/assets/QQQ/regime

Asset signals:

    curl http://127.0.0.1:8000/api/v1/assets/QQQ/signals

Governed explanation:

    curl -X POST http://127.0.0.1:8000/api/v1/ask \
      -H "Content-Type: application/json" \
      -d '{"symbol":"QQQ","question":"Why is QQQ buy_watch?"}'

## Expected behavior

The API should return JSON responses backed by Snowflake `MARTS` tables.

The `/ask` endpoint should return:

- the normalized symbol
- the original question
- a governed answer
- evidence used to construct the answer

## Troubleshooting

### Missing Snowflake environment variable

Symptom:

    KeyError: FINSIGNAL_SNOWFLAKE_ACCOUNT

Fix:

    set -a
    source .env
    set +a

Then restart `uvicorn`.

### 404 for a symbol

A `404` means the API is working, but no modeled mart context exists for that symbol yet.

Check whether the symbol exists in:

- `MARTS.MART_CURRENT_ASSET_SNAPSHOT`
- `MARTS.MART_ASSET_REGIME`
- `MARTS.MART_ASSET_SIGNAL`

### 500 response validation errors

A response validation error usually means the Python API schema does not match the data type returned by Snowflake. The API schemas should use typed fields such as `date`, `datetime`, `float`, and `str` instead of forcing every value into a string.
