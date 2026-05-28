from unittest.mock import Mock, patch

from ingestion.writers.s3_writer import S3RawWriter


@patch("ingestion.writers.s3_writer.boto3.client")
def test_write_market_prices_uploads_data_and_metadata_to_s3(mock_boto_client) -> None:
    mock_s3_client = Mock()
    mock_boto_client.return_value = mock_s3_client

    writer = S3RawWriter(bucket_name="finsignal-dev-raw")

    records = [
        {
            "provider_name": "static_sample",
            "symbol": "BTCUSD",
            "price_timestamp": "2026-05-22T00:00:00Z",
            "close_price": 69950.0,
            "raw_record": {"symbol": "BTCUSD"},
        }
    ]

    path = writer.write_market_prices(
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        records=records,
    )

    assert path.startswith("s3://finsignal-dev-raw/raw/provider=static_sample/")
    assert mock_s3_client.put_object.call_count == 2

    first_call = mock_s3_client.put_object.call_args_list[0].kwargs
    second_call = mock_s3_client.put_object.call_args_list[1].kwargs

    assert first_call["Bucket"] == "finsignal-dev-raw"
    assert first_call["Key"].endswith("/data.json")
    assert first_call["ContentType"] == "application/json"
    assert "sha256" in first_call["Metadata"]

    assert second_call["Bucket"] == "finsignal-dev-raw"
    assert second_call["Key"].endswith("/metadata.json")
    assert second_call["ContentType"] == "application/json"
