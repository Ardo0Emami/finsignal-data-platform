from __future__ import annotations

import json
from pathlib import Path

import pytest

from ingestion.loaders.raw_market_price_loader import load_raw_market_price_rows_from_file


def test_load_raw_market_price_rows_from_file_maps_payload_to_rows(tmp_path: Path) -> None:
    raw_file = tmp_path / "data.json"
    raw_file.write_text(
        json.dumps(
            {
                "provider": "static_sample",
                "dataset": "daily_prices",
                "symbol": "BTCUSD",
                "ingestion_run_id": "run-123",
                "ingested_at": "2026-05-22T01:02:03Z",
                "records": [
                    {
                        "provider_name": "static_sample",
                        "symbol": "BTCUSD",
                        "price_timestamp": "2026-05-20T00:00:00Z",
                        "open_price": 68000.0,
                        "high_price": 69200.0,
                        "low_price": 67500.0,
                        "close_price": 68900.0,
                        "adjusted_close_price": 68900.0,
                        "volume": 120000.0,
                        "raw_record": {
                            "symbol": "BTCUSD",
                            "close_price": 68900.0,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    rows = load_raw_market_price_rows_from_file(raw_file)

    assert len(rows) == 1

    row = rows[0]

    assert row.provider_name == "static_sample"
    assert row.dataset_name == "daily_prices"
    assert row.symbol == "BTCUSD"
    assert row.price_timestamp == "2026-05-20T00:00:00Z"
    assert row.open_price == 68000.0
    assert row.high_price == 69200.0
    assert row.low_price == 67500.0
    assert row.close_price == 68900.0
    assert row.adjusted_close_price == 68900.0
    assert row.volume == 120000.0
    assert row.raw_path == str(raw_file)
    assert row.ingestion_run_id == "run-123"
    assert row.ingested_at == "2026-05-22T01:02:03Z"
    assert row.raw_record == {
        "symbol": "BTCUSD",
        "close_price": 68900.0,
    }


def test_load_raw_market_price_rows_uses_full_record_when_raw_record_is_missing(
    tmp_path: Path,
) -> None:
    raw_file = tmp_path / "data.json"
    record = {
        "symbol": "QQQ",
        "price_timestamp": "2026-05-20T00:00:00Z",
        "close_price": 448.2,
    }

    raw_file.write_text(
        json.dumps(
            {
                "provider": "static_sample",
                "dataset": "daily_prices",
                "symbol": "QQQ",
                "ingestion_run_id": "run-456",
                "ingested_at": "2026-05-22T01:02:03Z",
                "records": [record],
            }
        ),
        encoding="utf-8",
    )

    rows = load_raw_market_price_rows_from_file(raw_file)

    assert len(rows) == 1
    assert rows[0].raw_record == record


def test_load_raw_market_price_rows_rejects_missing_records_list(tmp_path: Path) -> None:
    raw_file = tmp_path / "data.json"
    raw_file.write_text(
        json.dumps(
            {
                "provider": "static_sample",
                "dataset": "daily_prices",
                "symbol": "BTCUSD",
                "ingestion_run_id": "run-123",
                "ingested_at": "2026-05-22T01:02:03Z",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="records list"):
        load_raw_market_price_rows_from_file(raw_file)


def test_load_raw_market_price_rows_rejects_missing_close_price(tmp_path: Path) -> None:
    raw_file = tmp_path / "data.json"
    raw_file.write_text(
        json.dumps(
            {
                "provider": "static_sample",
                "dataset": "daily_prices",
                "symbol": "BTCUSD",
                "ingestion_run_id": "run-123",
                "ingested_at": "2026-05-22T01:02:03Z",
                "records": [
                    {
                        "symbol": "BTCUSD",
                        "price_timestamp": "2026-05-20T00:00:00Z",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="close_price"):
        load_raw_market_price_rows_from_file(raw_file)
