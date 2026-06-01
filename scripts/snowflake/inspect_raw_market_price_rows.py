from __future__ import annotations

import argparse
from pathlib import Path

from ingestion.loaders.raw_market_price_loader import load_raw_market_price_rows_from_file


def find_raw_data_files(raw_base_path: str | Path, limit: int) -> list[Path]:
    base_path = Path(raw_base_path)

    if not base_path.exists():
        raise FileNotFoundError(f"Raw base path does not exist: {base_path}")

    files = [
        path
        for path in base_path.rglob("data.json")
        if "dataset=daily_prices" in str(path)
    ]

    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)

    return files[:limit]


def inspect_raw_market_price_rows(raw_base_path: str | Path, limit: int) -> int:
    raw_files = find_raw_data_files(raw_base_path=raw_base_path, limit=limit)

    total_rows = 0

    for raw_file in raw_files:
        rows = load_raw_market_price_rows_from_file(raw_file)
        total_rows += len(rows)

        symbols = sorted({row.symbol for row in rows})
        run_ids = sorted({row.ingestion_run_id for row in rows})

        print(
            {
                "raw_file": str(raw_file),
                "row_count": len(rows),
                "symbols": symbols,
                "run_ids": run_ids,
            }
        )

    print({"files_inspected": len(raw_files), "total_rows": total_rows})

    return total_rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect local raw market price files as Snowflake-ready rows."
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
        help="Maximum number of latest raw data files to inspect.",
    )

    args = parser.parse_args()

    inspect_raw_market_price_rows(
        raw_base_path=args.raw_base_path,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
