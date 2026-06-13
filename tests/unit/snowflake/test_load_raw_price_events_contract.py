from __future__ import annotations

from pathlib import Path


def test_raw_price_event_loader_uses_staged_bulk_copy_pattern() -> None:
    script = Path("scripts/snowflake/load_raw_price_events.py").read_text(
        encoding="utf-8"
    )

    assert "PUT 'file://" in script
    assert "TARGET_TABLE = \"FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS\"" in script
    assert "COPY INTO {TARGET_TABLE}" in script
    assert "RAW_MARKET_PRICE_STAGE" in script
    assert "NDJSON_FORMAT" in script
    assert "ON_ERROR = ABORT_STATEMENT" in script
    assert "PURGE = FALSE" in script


def test_raw_price_event_loader_maps_expected_raw_event_columns() -> None:
    script = Path("scripts/snowflake/load_raw_price_events.py").read_text(
        encoding="utf-8"
    )

    assert "event_id" in script
    assert "event_type" in script
    assert "provider_name" in script
    assert "symbol" in script
    assert "price_timestamp" in script
    assert "close_price" in script
    assert "raw_path" in script
    assert "ingested_at" in script
    assert "raw_event" in script


def test_sample_price_event_creator_uses_price_event_model() -> None:
    script = Path("scripts/snowflake/create_sample_price_event_file.py").read_text(
        encoding="utf-8"
    )

    assert "PriceEvent.latest_price" in script
    assert "model_dump_json" in script
