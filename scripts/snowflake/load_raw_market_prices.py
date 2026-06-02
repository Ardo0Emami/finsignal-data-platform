from __future__ import annotations

import argparse
from pathlib import Path

from app.core.config import Settings
from ingestion.loaders.raw_market_price_loader import load_raw_market_price_rows_from_file
from ingestion.loaders.snowflake_market_price_loader import (
    SnowflakeMarketPriceLoader,
    create_snowflake_connection,
)
from scripts.snowflake.inspect_raw_market_price_rows import find_raw_data_files


def load_raw_market_price_files(
    *,
    raw_base_path: str | Path,
    limit: int,
) -> int:
    settings = Settings()
    raw_files = find_raw_data_files(raw_base_path=raw_base_path, limit=limit)

    connection = create_snowflake_connection(settings)

    try:
        loader = SnowflakeMarketPriceLoader(connection)
        total_loaded_rows = 0

        for raw_file in raw_files:
            rows = load_raw_market_price_rows_from_file(raw_file)
            loaded_rows = loader.load_rows(rows)
            total_loaded_rows += loaded_rows

            print(
                {
                    "raw_file": str(raw_file),
                    "loaded_rows": loaded_rows,
                }
            )

        print(
            {
                "files_loaded": len(raw_files),
                "total_loaded_rows": total_loaded_rows,
            }
        )

        return total_loaded_rows

    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load local raw market price files into Snowflake RAW_MARKET_PRICES."
    )
    parser.add_argument(
        "--raw-base-path",
        default="data/raw",
        help="Base path containing local raw market price files.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of latest raw data files to load.",
    )

    args = parser.parse_args()

    load_raw_market_price_files(
        raw_base_path=args.raw_base_path,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
