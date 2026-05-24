import json

from ingestion.writers.local_writer import LocalRawWriter


def test_write_market_prices_creates_data_and_metadata_files(tmp_path) -> None:
    writer = LocalRawWriter(str(tmp_path))

    records = [
        {
            "provider_name": "static_sample",
            "symbol": "BTCUSD",
            "price_timestamp": "2026-05-22T00:00:00Z",
            "close_price": 69950.0,
            "raw_record": {"symbol": "BTCUSD"},
        }
    ]

    data_path = writer.write_market_prices(
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        records=records,
    )

    data_file = tmp_path / data_path
    metadata_file = data_file.parent / "metadata.json"

    assert data_file.exists()
    assert metadata_file.exists()

    data_payload = json.loads(data_file.read_text(encoding="utf-8"))
    metadata_payload = json.loads(metadata_file.read_text(encoding="utf-8"))

    assert data_payload["provider"] == "static_sample"
    assert data_payload["dataset"] == "daily_prices"
    assert data_payload["symbol"] == "BTCUSD"
    assert len(data_payload["records"]) == 1

    assert metadata_payload["record_count"] == 1
    assert metadata_payload["schema_version"] == "1.0"
    assert metadata_payload["data_sha256"]
