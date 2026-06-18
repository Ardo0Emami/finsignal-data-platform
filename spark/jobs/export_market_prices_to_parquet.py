from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ingestion.loaders.raw_market_price_loader import iter_raw_market_price_rows


def export_market_prices_to_parquet(
    *,
    raw_root: Path,
    output_path: Path,
    limit: int | None = None,
) -> Path:
    rows = []

    for index, row in enumerate(iter_raw_market_price_rows(raw_root)):
        if limit is not None and index >= limit:
            break

        rows.append(
            {
                "provider_name": row.provider_name,
                "dataset_name": row.dataset_name,
                "symbol": row.symbol,
                "price_timestamp": row.price_timestamp,
                "price_date": row.price_timestamp.date(),
                "open_price": row.open_price,
                "high_price": row.high_price,
                "low_price": row.low_price,
                "close_price": row.close_price,
                "adjusted_close_price": row.adjusted_close_price,
                "volume": row.volume,
                "raw_path": row.raw_path,
                "ingestion_run_id": row.ingestion_run_id,
                "ingested_at": row.ingested_at,
            }
        )

    if not rows:
        raise ValueError(f"No raw market price rows found under {raw_root}")

    dataframe = pd.DataFrame(rows)
    output_path.mkdir(parents=True, exist_ok=True)
    dataframe.to_parquet(output_path, index=False)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export local raw market price JSON files to staged Parquet."
    )
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=Path("data/raw"),
        help="Root directory containing local raw market price JSON files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/staged/market_prices"),
        help="Output Parquet dataset directory.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of rows to export.",
    )
    args = parser.parse_args()

    path = export_market_prices_to_parquet(
        raw_root=args.raw_root,
        output_path=args.output,
        limit=args.limit,
    )

    print(path)


if __name__ == "__main__":
    main()
