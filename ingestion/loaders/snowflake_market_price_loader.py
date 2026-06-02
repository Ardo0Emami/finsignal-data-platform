from __future__ import annotations

import json
from typing import Any, Protocol

from app.core.config import Settings
from ingestion.loaders.raw_market_price_loader import RawMarketPriceRow

RAW_MARKET_PRICE_INSERT_SQL = """
INSERT INTO FINSIGNAL_DW.RAW.RAW_MARKET_PRICES (
    provider_name,
    dataset_name,
    symbol,
    price_timestamp,
    open_price,
    high_price,
    low_price,
    close_price,
    adjusted_close_price,
    volume,
    raw_path,
    ingestion_run_id,
    ingested_at,
    raw_record
)
SELECT
    %s,
    %s,
    %s,
    %s::TIMESTAMP_NTZ,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s::TIMESTAMP_NTZ,
    PARSE_JSON(%s)
"""


class SnowflakeCursor(Protocol):
    def executemany(self, command: str, seqparams: list[tuple[Any, ...]]) -> Any:
        ...

    def close(self) -> None:
        ...


class SnowflakeConnection(Protocol):
    def cursor(self) -> SnowflakeCursor:
        ...

    def commit(self) -> None:
        ...

    def close(self) -> None:
        ...


class SnowflakeMarketPriceLoader:
    def __init__(self, connection: SnowflakeConnection) -> None:
        self.connection = connection

    def load_rows(self, rows: list[RawMarketPriceRow]) -> int:
        if not rows:
            return 0

        cursor = self.connection.cursor()

        try:
            cursor.executemany(
                RAW_MARKET_PRICE_INSERT_SQL,
                [_row_to_insert_tuple(row) for row in rows],
            )
            self.connection.commit()
            return len(rows)
        finally:
            cursor.close()


def create_snowflake_connection(settings: Settings) -> SnowflakeConnection:
    missing_fields = [
        field_name
        for field_name in [
            "snowflake_account",
            "snowflake_user",
            "snowflake_password",
            "snowflake_warehouse",
        ]
        if not getattr(settings, field_name)
    ]

    if missing_fields:
        joined_fields = ", ".join(missing_fields)
        raise ValueError(f"Missing Snowflake settings: {joined_fields}")

    import snowflake.connector

    return snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        role=settings.snowflake_role,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
    )


def _row_to_insert_tuple(row: RawMarketPriceRow) -> tuple[Any, ...]:
    return (
        row.provider_name,
        row.dataset_name,
        row.symbol,
        row.price_timestamp,
        row.open_price,
        row.high_price,
        row.low_price,
        row.close_price,
        row.adjusted_close_price,
        row.volume,
        row.raw_path,
        row.ingestion_run_id,
        row.ingested_at,
        json.dumps(row.raw_record, sort_keys=True),
    )
