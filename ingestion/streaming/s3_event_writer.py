from __future__ import annotations

import json
from typing import Any

from ingestion.streaming.models import PriceEvent


class S3PriceEventWriter:
    def __init__(self, *, bucket_name: str, client: Any) -> None:
        self.bucket_name = bucket_name
        self.client = client

    def write(self, event: PriceEvent) -> str:
        ingestion_date = event.ingested_at.date().isoformat()

        key = (
            f"events/event_type={event.event_type}/"
            f"symbol={event.symbol}/"
            f"ingestion_date={ingestion_date}/"
            f"event_id={event.event_id}.json"
        )

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(event.model_dump(mode="json"), indent=2).encode("utf-8"),
            ContentType="application/json",
        )

        return f"s3://{self.bucket_name}/{key}"
