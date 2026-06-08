from __future__ import annotations

import json
from datetime import datetime, timezone

from ingestion.streaming.kinesis_producer import KinesisPriceEventProducer
from ingestion.streaming.models import PriceEvent


class FakeKinesisClient:
    def __init__(self) -> None:
        self.records: list[dict] = []

    def put_record(self, **kwargs: object) -> dict[str, str]:
        self.records.append(kwargs)
        return {"SequenceNumber": "1"}


def test_kinesis_producer_publishes_price_event_with_symbol_partition_key() -> None:
    client = FakeKinesisClient()
    producer = KinesisPriceEventProducer(
        stream_name="finsignal-dev-price-events",
        client=client,
    )
    event = PriceEvent.latest_price(
        provider_name="static_sample",
        symbol="QQQ",
        close_price=450.25,
        price_timestamp=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )

    event_id = producer.publish(event)

    assert event_id == event.event_id
    assert len(client.records) == 1

    record = client.records[0]
    assert record["StreamName"] == "finsignal-dev-price-events"
    assert record["PartitionKey"] == "QQQ"

    payload = json.loads(record["Data"].decode("utf-8"))
    assert payload["event_id"] == event.event_id
    assert payload["symbol"] == "QQQ"
    assert payload["close_price"] == 450.25
