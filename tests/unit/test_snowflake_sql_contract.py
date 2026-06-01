from __future__ import annotations

from pathlib import Path


def test_snowflake_database_script_defines_expected_schemas() -> None:
    sql = Path("scripts/snowflake/001_create_database.sql").read_text(
        encoding="utf-8"
    )

    assert "CREATE DATABASE IF NOT EXISTS FINSIGNAL_DW" in sql
    assert "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.RAW" in sql
    assert "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.STAGING" in sql
    assert "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.INTERMEDIATE" in sql
    assert "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.MARTS" in sql
    assert "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.AUDIT" in sql
    assert "CREATE SCHEMA IF NOT EXISTS FINSIGNAL_DW.SANDBOX" in sql


def test_snowflake_raw_tables_script_defines_market_price_table() -> None:
    sql = Path("scripts/snowflake/002_create_raw_tables.sql").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.RAW.RAW_MARKET_PRICES" in sql
    assert "provider_name STRING NOT NULL" in sql
    assert "dataset_name STRING NOT NULL" in sql
    assert "symbol STRING NOT NULL" in sql
    assert "price_timestamp TIMESTAMP_NTZ NOT NULL" in sql
    assert "close_price FLOAT NOT NULL" in sql
    assert "raw_path STRING NOT NULL" in sql
    assert "ingestion_run_id STRING NOT NULL" in sql
    assert "raw_record VARIANT NOT NULL" in sql


def test_snowflake_raw_tables_script_defines_price_event_table() -> None:
    sql = Path("scripts/snowflake/002_create_raw_tables.sql").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS" in sql
    assert "event_id STRING NOT NULL" in sql
    assert "event_type STRING NOT NULL" in sql
    assert "raw_event VARIANT NOT NULL" in sql


def test_snowflake_audit_tables_script_defines_ingestion_audit_table() -> None:
    sql = Path("scripts/snowflake/003_create_audit_tables.sql").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.AUDIT.INGESTION_RUNS" in sql
    assert "run_id STRING NOT NULL" in sql
    assert "status STRING NOT NULL" in sql
    assert "records_extracted INTEGER NOT NULL" in sql
    assert "records_written INTEGER NOT NULL" in sql
    assert "error_message STRING" in sql


def test_snowflake_audit_tables_script_defines_data_quality_table() -> None:
    sql = Path("scripts/snowflake/003_create_audit_tables.sql").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.AUDIT.DATA_QUALITY_RESULTS" in sql
    assert "check_name STRING NOT NULL" in sql
    assert "failed_row_count INTEGER NOT NULL" in sql
    assert "details VARIANT" in sql
