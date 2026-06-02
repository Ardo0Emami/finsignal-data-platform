# INGESTION_RUNS Contract

`FINSIGNAL_DW.AUDIT.INGESTION_RUNS` stores one audit record for each symbol-level ingestion attempt.

This table is used for lineage, operational debugging, data quality checks, and downstream filtering.

## Grain

One row represents:

    one provider
    one dataset
    one symbol
    one ingestion run

A run may succeed or fail.

## Table

    FINSIGNAL_DW.AUDIT.INGESTION_RUNS

## Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `run_id` | STRING | yes | Unique ingestion run identifier. |
| `provider_name` | STRING | yes | Source provider used for extraction. |
| `dataset_name` | STRING | yes | Dataset identifier, currently `daily_prices`. |
| `symbol` | STRING | yes | Asset symbol being ingested. |
| `status` | STRING | yes | `succeeded` or `failed`. |
| `started_at` | TIMESTAMP_NTZ | yes | Ingestion start timestamp. |
| `completed_at` | TIMESTAMP_NTZ | no | Ingestion completion timestamp. |
| `records_extracted` | INTEGER | yes | Number of records extracted from the provider. |
| `records_written` | INTEGER | yes | Number of records written to raw storage. |
| `raw_path` | STRING | no | Raw file path for successful runs. |
| `error_message` | STRING | no | Failure message for failed runs. |
| `created_at` | TIMESTAMP_NTZ | yes | Warehouse insert timestamp. |

## Status Values

Allowed statuses:

    succeeded
    failed

## Relationship to Raw Data

Successful runs should have:

    records_extracted > 0
    records_written > 0
    raw_path is not null

Failed runs should have:

    status = failed
    error_message is not null

## Usage

This table supports:

- tracing raw files to ingestion runs
- filtering downstream models to successful runs
- identifying provider failures
- validating record counts
- operational monitoring
