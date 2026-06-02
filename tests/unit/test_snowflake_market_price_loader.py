from __future__ import annotations

import json
from typing import Any

import pytest

from app.core.config import Settings
from ingestion.loaders.raw_market_price_loader import RawMarketPriceRow
from ingestion.loaders.snowflake_market_price_loader import (
    RAW_MARKET_PRICE_INSERT_SQL,
    SnowflakeMarketPriceLoader,
    create_snowflake_connection,
)


class FakeCursor:
    def __init__(self) -> None:
        self.executed_command: str | None = None
        self.executed_params: list[tuple[Any, ...]] = []
        self.closed = False

    def executemany(self, command: str, seqparams: list[tuple[Any, ...]]) -> None:
        self.executed_command = command
        self.executed_params = seqparams

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_instance = FakeCursor()
        self.committed = False

    def cursor(self) -> FakeCursor:
        return self.cursor_instance

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        pass


def _row() -> RawMarketPriceRow:
    return RawMarketPriceRow(
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        price_timestamp="2026-06-01T00:00:00Z",
        open_price=100.0,
        high_price=110.0,
        low_price=95.0,
        close_price=105.0,
        adjusted_close_price=105.0,
        volume=12345.0,
        raw_path="data/raw/sample/data.json",
        ingestion_run_id="run-123",
        ingested_at="2026-06-01T01:00:00Z",
        raw_record={"symbol": "BTCUSD", "close_price": 105.0},
    )


def test_snowflake_loader_inserts_raw_market_price_rows() -> None:
    connection = FakeConnection()
    loader = SnowflakeMarketPriceLoader(connection)

    loaded_count = loader.load_rows([_row()])

    assert loaded_count == 1
    assert connection.committed is True
    assert connection.cursor_instance.closed is True
    assert connection.cursor_instance.executed_command == RAW_MARKET_PRICE_INSERT_SQL
    assert len(connection.cursor_instance.executed_params) == 1

    inserted_row = connection.cursor_instance.executed_params[0]

    assert inserted_row[0] == "static_sample"
    assert inserted_row[1] == "daily_prices"
    assert inserted_row[2] == "BTCUSD"
    assert inserted_row[7] == 105.0
    assert inserted_row[11] == "run-123"
    assert json.loads(inserted_row[13]) == {
        "symbol": "BTCUSD",
        "close_price": 105.0,
    }


def test_snowflake_loader_skips_empty_row_list() -> None:
    connection = FakeConnection()
    loader = SnowflakeMarketPriceLoader(connection)

    loaded_count = loader.load_rows([])

    assert loaded_count == 0
    assert connection.committed is False
    assert connection.cursor_instance.executed_command is None


def test_create_snowflake_connection_requires_connection_settings() -> None:
    settings = Settings(
        snowflake_account=None,
        snowflake_user=None,
        snowflake_password=None,
        snowflake_warehouse=None,
    )

    with pytest.raises(ValueError, match="snowflake_account"):
        create_snowflake_connection(settings)
