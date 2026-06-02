from __future__ import annotations

from pathlib import Path


def test_raw_load_verification_sql_checks_symbol_row_counts() -> None:
    sql = Path("scripts/snowflake/004_verify_raw_load.sql").read_text(
        encoding="utf-8"
    )

    assert "FINSIGNAL_DW.RAW.RAW_MARKET_PRICES" in sql
    assert "COUNT(*) AS row_count" in sql
    assert "MIN(price_timestamp)" in sql
    assert "MAX(price_timestamp)" in sql
    assert "GROUP BY" in sql


def test_raw_load_verification_sql_checks_ingestion_lineage() -> None:
    sql = Path("scripts/snowflake/004_verify_raw_load.sql").read_text(
        encoding="utf-8"
    )

    assert "ingestion_run_id" in sql
    assert "raw_path" in sql
    assert "ORDER BY" in sql
