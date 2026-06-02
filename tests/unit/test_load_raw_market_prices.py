from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from scripts.snowflake import load_raw_market_prices


class FakeSnowflakeLoader:
    def __init__(self, connection: object) -> None:
        self.connection = connection

    def load_rows(self, rows: list[object]) -> int:
        return len(rows)


class FakeSnowflakeConnection:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


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


def test_load_raw_market_price_files_loads_rows_and_closes_connection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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

    fake_connection = FakeSnowflakeConnection()

    def fake_create_connection(settings: object) -> FakeSnowflakeConnection:
        return fake_connection

    monkeypatch.setattr(
        load_raw_market_prices,
        "create_snowflake_connection",
        fake_create_connection,
    )
    monkeypatch.setattr(
        load_raw_market_prices,
        "SnowflakeMarketPriceLoader",
        FakeSnowflakeLoader,
    )

    loaded_count = load_raw_market_prices.load_raw_market_price_files(
        raw_base_path=tmp_path,
        limit=5,
    )

    assert loaded_count == 2
    assert fake_connection.closed is True


def test_load_raw_market_price_files_closes_connection_on_loader_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw_file = (
        tmp_path
        / "provider=static_sample"
        / "dataset=daily_prices"
        / "symbol=QQQ"
        / "ingestion_date=2026-06-01"
        / "run_id=run-456"
        / "data.json"
    )
    _write_raw_file(raw_file, symbol="QQQ", run_id="run-456")

    fake_connection = FakeSnowflakeConnection()

    class FailingLoader:
        def __init__(self, connection: object) -> None:
            self.connection = connection

        def load_rows(self, rows: list[Any]) -> int:
            raise RuntimeError("snowflake load failed")

    def fake_create_connection(settings: object) -> FakeSnowflakeConnection:
        return fake_connection

    monkeypatch.setattr(
        load_raw_market_prices,
        "create_snowflake_connection",
        fake_create_connection,
    )
    monkeypatch.setattr(
        load_raw_market_prices,
        "SnowflakeMarketPriceLoader",
        FailingLoader,
    )

    with pytest.raises(RuntimeError, match="snowflake load failed"):
        load_raw_market_prices.load_raw_market_price_files(
            raw_base_path=tmp_path,
            limit=5,
        )

    assert fake_connection.closed is True
