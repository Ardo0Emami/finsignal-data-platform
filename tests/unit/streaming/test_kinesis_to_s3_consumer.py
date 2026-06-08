from __future__ import annotations

import json
from datetime import datetime, timezone

from ingestion.streaming.kinesis_consumer import KinesisToS3PriceEventConsumer
from ingestion.streaming.models import PriceEvent
from ingestion.streaming.s3_event_writer import S3PriceEventWriter


class FakeKinesisClient:
    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def get_records(self, **kwargs: object) -> dict[str, list[dict]]:
        assert kwargs["ShardIterator"] == "fake-iterator"
        assert kwargs["Limit"] == 100
        return {"Records": self.records}


class FakeS3Client:
    def __init__(self) -> None:
        self.objects: list[dict] = []

    def put_object(self, **kwargs: object) -> dict[str, str]:
        self.objects.append(kwargs)
        return {"ETag": "fake-etag"}


def test_kinesis_consumer_writes_records_to_s3() -> None:
    event = PriceEvent.latest_price(
        provider_name="static_sample",
        symbol="QQQ",
        close_price=450.25,
        price_timestamp=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )

    kinesis_client = FakeKinesisClient(
        records=[
            {
                "Data": json.dumps(event.model_dump(mode="json")).encode("utf-8"),
            }
        ]
    )
    s3_client = FakeS3Client()
    s3_writer = S3PriceEventWriter(bucket_name="finsignal-dev-raw", client=s3_client)

    consumer = KinesisToS3PriceEventConsumer(
        stream_name="finsignal-dev-price-events",
        kinesis_client=kinesis_client,
        s3_writer=s3_writer,
    )

    written_paths = consumer.consume_once(shard_iterator="fake-iterator")

    assert len(written_paths) == 1
    assert written_paths[0].startswith("s3://finsignal-dev-raw/events/")
    assert len(s3_client.objects) == 1
