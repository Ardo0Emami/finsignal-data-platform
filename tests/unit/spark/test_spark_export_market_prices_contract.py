from __future__ import annotations

from pathlib import Path


def test_export_market_prices_to_parquet_reads_local_raw_data_json_files() -> None:
    script = Path("spark/jobs/export_market_prices_to_parquet.py").read_text(
        encoding="utf-8"
    )

    assert 'raw_root.rglob("data.json")' in script
    assert "json.loads" in script
    assert "to_parquet" in script
    assert "provider_name" in script
    assert "dataset_name" in script
    assert "symbol" in script
    assert "price_timestamp" in script
    assert "close_price" in script
    assert "raw_path" in script
    assert "ingestion_run_id" in script


def test_export_market_prices_to_parquet_writes_a_parquet_file_inside_dataset_dir() -> None:
    script = Path("spark/jobs/export_market_prices_to_parquet.py").read_text(
        encoding="utf-8"
    )

    assert 'default=Path("data/raw")' in script
    assert 'default=Path("data/staged/market_prices")' in script
    assert 'output_path / "market_prices.parquet"' in script
    assert "return parquet_file" in script
