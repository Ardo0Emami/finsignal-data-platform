from __future__ import annotations

import json

from ingestion.lambda_handlers.latest_price_ingestion import (
    build_price_event_from_lambda_event,
    handle_latest_price_event,
)


class FakeKinesisClient:
    def __init__(self) -> None:
        self.records: list[dict] = []

    def put_record(self, **kwargs: object) -> dict[str, str]:
        self.records.append(kwargs)
        return {"SequenceNumber": "1"}


class FakeS3Client:
    def __init__(self) -> None:
        self.objects: list[dict] = []

    def put_object(self, **kwargs: object) -> dict[str, str]:
        self.objects.append(kwargs)
        return {"ETag": "fake-etag"}


def test_build_price_event_from_lambda_event() -> None:
    event = build_price_event_from_lambda_event(
        {
            "provider_name": "static_sample",
            "symbol": "btcusd",
            "close_price": 69000.0,
            "price_timestamp": "2026-05-01T10:00:00Z",
        }
    )

    assert event.provider_name == "static_sample"
    assert event.symbol == "BTCUSD"
    assert event.close_price == 69000.0
    assert event.price_timestamp.isoformat() == "2026-05-01T10:00:00+00:00"
    assert event.raw_event["symbol"] == "btcusd"


def test_handle_latest_price_event_publishes_to_kinesis_and_writes_to_s3() -> None:
    kinesis_client = FakeKinesisClient()
    s3_client = FakeS3Client()

    result = handle_latest_price_event(
        event={
            "provider_name": "static_sample",
            "symbol": "QQQ",
            "close_price": 450.25,
            "price_timestamp": "2026-05-01T10:00:00Z",
        },
        kinesis_client=kinesis_client,
        s3_client=s3_client,
        stream_name="finsignal-dev-price-events",
        bucket_name="finsignal-dev-raw",
    )

    assert result["event_type"] == "PRICE_TICK"
    assert result["symbol"] == "QQQ"
    assert result["provider_name"] == "static_sample"
    assert result["raw_s3_path"].startswith("s3://finsignal-dev-raw/events/")

    assert len(kinesis_client.records) == 1
    kinesis_record = kinesis_client.records[0]
    assert kinesis_record["StreamName"] == "finsignal-dev-price-events"
    assert kinesis_record["PartitionKey"] == "QQQ"

    kinesis_payload = json.loads(kinesis_record["Data"].decode("utf-8"))
    assert kinesis_payload["event_id"] == result["event_id"]
    assert kinesis_payload["symbol"] == "QQQ"

    assert len(s3_client.objects) == 1
    s3_object = s3_client.objects[0]
    assert s3_object["Bucket"] == "finsignal-dev-raw"
    assert "events/event_type=PRICE_TICK/symbol=QQQ/" in s3_object["Key"]

    s3_payload = json.loads(s3_object["Body"].decode("utf-8"))
    assert s3_payload["event_id"] == result["event_id"]
    assert s3_payload["close_price"] == 450.25
