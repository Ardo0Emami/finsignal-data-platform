from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Protocol
from uuid import uuid4

from app.core.config import Settings
from ingestion.loaders.raw_market_price_loader import RawMarketPriceRow

RAW_MARKET_PRICE_STAGE = "FINSIGNAL_DW.RAW.RAW_MARKET_PRICE_STAGE"
RAW_MARKET_PRICE_TABLE = "FINSIGNAL_DW.RAW.RAW_MARKET_PRICES"
NDJSON_FILE_FORMAT = "FINSIGNAL_DW.RAW.NDJSON_FORMAT"


class SnowflakeCursor(Protocol):
    def execute(self, command: str) -> Any:
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

        load_batch_id = f"load_batch_id={uuid4()}"
        stage_path = f"{RAW_MARKET_PRICE_STAGE}/{load_batch_id}"

        cursor = self.connection.cursor()

        try:
            with TemporaryDirectory() as temp_dir:
                load_file = Path(temp_dir) / f"raw_market_prices_{uuid4()}.json"
                write_raw_market_price_load_file(rows=rows, output_path=load_file)

                cursor.execute(_build_put_sql(load_file=load_file, stage_path=stage_path))
                cursor.execute(_build_copy_sql(stage_path=stage_path))

            self.connection.commit()
            return len(rows)

        finally:
            cursor.close()


def create_snowflake_connection(settings: Settings) -> SnowflakeConnection:
    required_fields = [
        "snowflake_account",
        "snowflake_user",
        "snowflake_warehouse",
    ]

    if settings.snowflake_authenticator in {"snowflake", "username_password_mfa"}:
        required_fields.append("snowflake_password")

    missing_fields = [
        field_name
        for field_name in required_fields
        if not getattr(settings, field_name)
    ]

    if missing_fields:
        joined_fields = ", ".join(missing_fields)
        raise ValueError(f"Missing Snowflake settings: {joined_fields}")

    import snowflake.connector

    connection_kwargs = {
        "account": settings.snowflake_account,
        "user": settings.snowflake_user,
        "role": settings.snowflake_role,
        "warehouse": settings.snowflake_warehouse,
        "database": settings.snowflake_database,
        "schema": settings.snowflake_schema,
        "authenticator": settings.snowflake_authenticator,
    }

    if settings.snowflake_authenticator in {"snowflake", "username_password_mfa"}:
        connection_kwargs["password"] = settings.snowflake_password

    return snowflake.connector.connect(**connection_kwargs)


def write_raw_market_price_load_file(
    *,
    rows: list[RawMarketPriceRow],
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(_row_to_load_object(row), sort_keys=True))
            file.write("\n")

    return path


def _build_put_sql(*, load_file: Path, stage_path: str) -> str:
    local_file_uri = f"file://{load_file.as_posix()}"
    return f"PUT '{local_file_uri}' @{stage_path} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"


def _build_copy_sql(*, stage_path: str) -> str:
    return f"""
COPY INTO {RAW_MARKET_PRICE_TABLE} (
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
FROM (
    SELECT
        $1:provider_name::STRING,
        $1:dataset_name::STRING,
        $1:symbol::STRING,
        $1:price_timestamp::TIMESTAMP_NTZ,
        $1:open_price::FLOAT,
        $1:high_price::FLOAT,
        $1:low_price::FLOAT,
        $1:close_price::FLOAT,
        $1:adjusted_close_price::FLOAT,
        $1:volume::FLOAT,
        $1:raw_path::STRING,
        $1:ingestion_run_id::STRING,
        $1:ingested_at::TIMESTAMP_NTZ,
        $1:raw_record::VARIANT
    FROM @{stage_path}
)
FILE_FORMAT = (FORMAT_NAME = {NDJSON_FILE_FORMAT})
ON_ERROR = ABORT_STATEMENT
PURGE = FALSE
"""


def _row_to_load_object(row: RawMarketPriceRow) -> dict[str, Any]:
    return {
        "provider_name": row.provider_name,
        "dataset_name": row.dataset_name,
        "symbol": row.symbol,
        "price_timestamp": row.price_timestamp,
        "open_price": row.open_price,
        "high_price": row.high_price,
        "low_price": row.low_price,
        "close_price": row.close_price,
        "adjusted_close_price": row.adjusted_close_price,
        "volume": row.volume,
        "raw_path": row.raw_path,
        "ingestion_run_id": row.ingestion_run_id,
        "ingested_at": row.ingested_at,
        "raw_record": row.raw_record,
    }
