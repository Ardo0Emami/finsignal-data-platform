from __future__ import annotations

from pathlib import Path


def test_export_market_prices_to_parquet_uses_raw_market_price_loader() -> None:
    script = Path("spark/jobs/export_market_prices_to_parquet.py").read_text(
        encoding="utf-8"
    )

    assert "iter_raw_market_price_rows" in script
    assert "to_parquet" in script
    assert "provider_name" in script
    assert "dataset_name" in script
    assert "symbol" in script
    assert "price_timestamp" in script
    assert "close_price" in script
    assert "raw_path" in script
    assert "ingestion_run_id" in script


def test_export_market_prices_to_parquet_has_local_defaults() -> None:
    script = Path("spark/jobs/export_market_prices_to_parquet.py").read_text(
        encoding="utf-8"
    )

    assert 'default=Path("data/raw")' in script
    assert 'default=Path("data/staged/market_prices")' in script
