from __future__ import annotations

import json
from datetime import datetime, timezone

from ingestion.streaming.models import PriceEvent
from ingestion.streaming.s3_event_writer import S3PriceEventWriter


class FakeS3Client:
    def __init__(self) -> None:
        self.objects: list[dict] = []

    def put_object(self, **kwargs: object) -> dict[str, str]:
        self.objects.append(kwargs)
        return {"ETag": "fake-etag"}


def test_s3_price_event_writer_writes_partitioned_event_path() -> None:
    client = FakeS3Client()
    writer = S3PriceEventWriter(bucket_name="finsignal-dev-raw", client=client)

    event = PriceEvent.latest_price(
        provider_name="static_sample",
        symbol="BTCUSD",
        close_price=69000.0,
        price_timestamp=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )

    path = writer.write(event)

    assert path.startswith("s3://finsignal-dev-raw/events/event_type=PRICE_TICK/")
    assert "symbol=BTCUSD" in path
    assert f"event_id={event.event_id}.json" in path
    assert len(client.objects) == 1

    stored = client.objects[0]
    assert stored["Bucket"] == "finsignal-dev-raw"
    assert stored["ContentType"] == "application/json"

    payload = json.loads(stored["Body"].decode("utf-8"))
    assert payload["event_id"] == event.event_id
    assert payload["symbol"] == "BTCUSD"
