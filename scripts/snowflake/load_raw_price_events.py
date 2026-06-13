from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from uuid import uuid4

import snowflake.connector

from app.core.config import Settings
from ingestion.streaming.raw_price_event_loader import (
    load_raw_price_event_row_from_file,
    raw_price_event_row_to_snowflake_json,
)

STAGE_NAME = "FINSIGNAL_DW.RAW.RAW_MARKET_PRICE_STAGE"
FILE_FORMAT_NAME = "FINSIGNAL_DW.RAW.NDJSON_FORMAT"
TARGET_TABLE = "FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS"


def _connect(settings: Settings):
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


def _write_ndjson_load_file(event_files: list[Path]) -> Path:
    rows = []

    for event_file in event_files:
        row = load_raw_price_event_row_from_file(event_file)
        rows.append(raw_price_event_row_to_snowflake_json(row))

    output_path = Path(tempfile.gettempdir()) / f"finsignal_raw_price_events_{uuid4()}.ndjson"

    with output_path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, default=str))
            file.write("\n")

    return output_path


def load_raw_price_events(event_files: list[Path]) -> dict[str, object]:
    if not event_files:
        return {
            "status": "skipped",
            "reason": "no event files provided",
            "rows_loaded": 0,
        }

    settings = Settings()
    load_batch_id = str(uuid4())
    load_file = _write_ndjson_load_file(event_files)
    stage_prefix = f"price_event_load_batch_id={load_batch_id}"

    connection = _connect(settings)
    cursor = connection.cursor()

    try:
        put_sql = (
            f"PUT 'file://{load_file.as_posix()}' "
            f"@{STAGE_NAME}/{stage_prefix} "
            "AUTO_COMPRESS=FALSE "
            "OVERWRITE=TRUE"
        )
        cursor.execute(put_sql)

        copy_sql = f"""
            COPY INTO {TARGET_TABLE} (
                event_id,
                event_type,
                provider_name,
                symbol,
                price_timestamp,
                close_price,
                raw_path,
                ingested_at,
                raw_event
            )
            FROM (
                SELECT
                    $1:event_id::STRING,
                    $1:event_type::STRING,
                    $1:provider_name::STRING,
                    $1:symbol::STRING,
                    $1:price_timestamp::TIMESTAMP_NTZ,
                    $1:close_price::FLOAT,
                    $1:raw_path::STRING,
                    $1:ingested_at::TIMESTAMP_NTZ,
                    $1:raw_event::VARIANT
                FROM @{STAGE_NAME}/{stage_prefix}
            )
            FILE_FORMAT = (FORMAT_NAME = {FILE_FORMAT_NAME})
            ON_ERROR = ABORT_STATEMENT
            PURGE = FALSE
        """
        cursor.execute(copy_sql)
        copy_results = cursor.fetchall()

        return {
            "status": "succeeded",
            "event_files": [str(path) for path in event_files],
            "rows_loaded": len(event_files),
            "load_batch_id": load_batch_id,
            "copy_results": copy_results,
        }
    finally:
        cursor.close()
        connection.close()
        load_file.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load raw price event JSON files into Snowflake RAW_PRICE_EVENTS."
    )
    parser.add_argument(
        "event_files",
        nargs="+",
        type=Path,
        help="One or more local price event JSON files.",
    )
    args = parser.parse_args()

    result = load_raw_price_events(args.event_files)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
