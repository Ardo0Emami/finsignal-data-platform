from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core.config import Settings
from ingestion.loaders.raw_market_price_loader import RawMarketPriceRow
from ingestion.loaders.snowflake_market_price_loader import (
    RAW_MARKET_PRICE_STAGE,
    SnowflakeMarketPriceLoader,
    _build_copy_sql,
    _build_put_sql,
    create_snowflake_connection,
    write_raw_market_price_load_file,
)


class FakeCursor:
    def __init__(self) -> None:
        self.executed_commands: list[str] = []
        self.closed = False

    def execute(self, command: str) -> None:
        self.executed_commands.append(command)

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


def _row(symbol: str = "BTCUSD") -> RawMarketPriceRow:
    return RawMarketPriceRow(
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol=symbol,
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
        raw_record={"symbol": symbol, "close_price": 105.0},
    )


def test_write_raw_market_price_load_file_writes_ndjson_rows(tmp_path: Path) -> None:
    output_path = tmp_path / "raw_market_prices.json"

    write_raw_market_price_load_file(
        rows=[_row("BTCUSD"), _row("QQQ")],
        output_path=output_path,
    )

    lines = output_path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2

    first_row = json.loads(lines[0])
    second_row = json.loads(lines[1])

    assert first_row["symbol"] == "BTCUSD"
    assert first_row["close_price"] == 105.0
    assert first_row["raw_record"] == {
        "symbol": "BTCUSD",
        "close_price": 105.0,
    }
    assert second_row["symbol"] == "QQQ"


def test_build_put_sql_quotes_local_file_uri_and_uses_unique_stage_path(
    tmp_path: Path,
) -> None:
    load_file = tmp_path / "raw_market_prices.json"
    stage_path = f"{RAW_MARKET_PRICE_STAGE}/load_batch_id=abc"

    sql = _build_put_sql(load_file=load_file, stage_path=stage_path)

    assert sql.startswith("PUT 'file://")
    assert load_file.as_posix() in sql
    assert f"@{stage_path}" in sql
    assert "AUTO_COMPRESS=FALSE" in sql
    assert "OVERWRITE=TRUE" in sql


def test_build_copy_sql_copies_only_scoped_stage_prefix() -> None:
    stage_path = f"{RAW_MARKET_PRICE_STAGE}/load_batch_id=abc"

    sql = _build_copy_sql(stage_path=stage_path)

    assert f"FROM @{stage_path}" in sql
    assert "COPY INTO FINSIGNAL_DW.RAW.RAW_MARKET_PRICES" in sql
    assert "FILE_FORMAT = (FORMAT_NAME = FINSIGNAL_DW.RAW.NDJSON_FORMAT)" in sql
    assert "ON_ERROR = ABORT_STATEMENT" in sql
    assert "PURGE = FALSE" in sql


def test_snowflake_loader_uses_stage_prefix_and_copy_into() -> None:
    connection = FakeConnection()
    loader = SnowflakeMarketPriceLoader(connection)

    loaded_count = loader.load_rows([_row()])

    assert loaded_count == 1
    assert connection.committed is True
    assert connection.cursor_instance.closed is True
    assert len(connection.cursor_instance.executed_commands) == 2

    put_command = connection.cursor_instance.executed_commands[0]
    copy_command = connection.cursor_instance.executed_commands[1]

    assert put_command.startswith("PUT 'file://")
    assert f"@{RAW_MARKET_PRICE_STAGE}/load_batch_id=" in put_command
    assert f"FROM @{RAW_MARKET_PRICE_STAGE}/load_batch_id=" in copy_command
    assert "PURGE = FALSE" in copy_command


def test_snowflake_loader_skips_empty_row_list() -> None:
    connection = FakeConnection()
    loader = SnowflakeMarketPriceLoader(connection)

    loaded_count = loader.load_rows([])

    assert loaded_count == 0
    assert connection.committed is False
    assert connection.cursor_instance.executed_commands == []


def test_create_snowflake_connection_requires_connection_settings() -> None:
    settings = Settings(
        snowflake_account=None,
        snowflake_user=None,
        snowflake_password=None,
        snowflake_warehouse=None,
    )

    with pytest.raises(ValueError, match="snowflake_account"):
        create_snowflake_connection(settings)
