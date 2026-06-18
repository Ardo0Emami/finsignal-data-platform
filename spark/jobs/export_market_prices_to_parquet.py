from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def _iter_raw_market_price_payloads(raw_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for data_file in sorted(raw_root.rglob("data.json")):
        payload = json.loads(data_file.read_text(encoding="utf-8"))

        provider_name = payload["provider"]
        dataset_name = payload["dataset"]
        symbol = payload["symbol"]
        ingestion_run_id = payload["ingestion_run_id"]
        ingested_at = payload["ingested_at"]

        for record in payload["records"]:
            rows.append(
                {
                    "provider_name": provider_name,
                    "dataset_name": dataset_name,
                    "symbol": symbol,
                    "price_timestamp": record["price_timestamp"],
                    "price_date": record["price_timestamp"][:10],
                    "open_price": record.get("open_price"),
                    "high_price": record.get("high_price"),
                    "low_price": record.get("low_price"),
                    "close_price": record["close_price"],
                    "adjusted_close_price": record.get("adjusted_close_price"),
                    "volume": record.get("volume"),
                    "raw_path": str(data_file),
                    "ingestion_run_id": ingestion_run_id,
                    "ingested_at": ingested_at,
                }
            )

    return rows


def export_market_prices_to_parquet(
    *,
    raw_root: Path,
    output_path: Path,
    limit: int | None = None,
) -> Path:
    rows = _iter_raw_market_price_payloads(raw_root)

    if limit is not None:
        rows = rows[:limit]

    if not rows:
        raise ValueError(f"No raw market price rows found under {raw_root}")

    dataframe = pd.DataFrame(rows)

    output_path.mkdir(parents=True, exist_ok=True)
    parquet_file = output_path / "market_prices.parquet"
    dataframe.to_parquet(parquet_file, index=False)

    return parquet_file


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
