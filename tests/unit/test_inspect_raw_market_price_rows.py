from __future__ import annotations

import json
from pathlib import Path

from scripts.snowflake.inspect_raw_market_price_rows import (
    find_raw_data_files,
    inspect_raw_market_price_rows,
)


def _write_raw_file(path: Path, symbol: str, run_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "provider": "static_sample",
                "dataset": "daily_prices",
                "symbol": symbol,
                "ingestion_run_id": run_id,
                "ingested_at": "2026-06-01T00:00:00Z",
                "records": [
                    {
                        "symbol": symbol,
                        "price_timestamp": "2026-06-01T00:00:00Z",
                        "close_price": 100.0,
                    },
                    {
                        "symbol": symbol,
                        "price_timestamp": "2026-06-02T00:00:00Z",
                        "close_price": 101.0,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )


def test_find_raw_data_files_returns_latest_daily_price_files(tmp_path: Path) -> None:
    older_file = (
        tmp_path
        / "provider=static_sample"
        / "dataset=daily_prices"
        / "symbol=BTCUSD"
        / "ingestion_date=2026-06-01"
        / "run_id=older"
        / "data.json"
    )
    newer_file = (
        tmp_path
        / "provider=static_sample"
        / "dataset=daily_prices"
        / "symbol=QQQ"
        / "ingestion_date=2026-06-01"
        / "run_id=newer"
        / "data.json"
    )

    _write_raw_file(older_file, symbol="BTCUSD", run_id="older")
    _write_raw_file(newer_file, symbol="QQQ", run_id="newer")

    older_file.touch()
    newer_file.touch()

    files = find_raw_data_files(raw_base_path=tmp_path, limit=1)

    assert files == [newer_file]


def test_inspect_raw_market_price_rows_returns_total_row_count(tmp_path: Path) -> None:
    raw_file = (
        tmp_path
        / "provider=static_sample"
        / "dataset=daily_prices"
        / "symbol=BTCUSD"
        / "ingestion_date=2026-06-01"
        / "run_id=run-123"
        / "data.json"
    )

    _write_raw_file(raw_file, symbol="BTCUSD", run_id="run-123")

    total_rows = inspect_raw_market_price_rows(raw_base_path=tmp_path, limit=5)

    assert total_rows == 2
