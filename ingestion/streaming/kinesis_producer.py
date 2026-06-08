from __future__ import annotations

import json
from typing import Any

from ingestion.streaming.models import PriceEvent


class KinesisPriceEventProducer:
    def __init__(self, *, stream_name: str, client: Any) -> None:
        self.stream_name = stream_name
        self.client = client

    def publish(self, event: PriceEvent) -> str:
        payload = event.model_dump(mode="json")

        self.client.put_record(
            StreamName=self.stream_name,
            Data=json.dumps(payload).encode("utf-8"),
            PartitionKey=event.symbol,
        )

        return event.event_id
