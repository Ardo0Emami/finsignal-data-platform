from __future__ import annotations

import json
from typing import Any

from ingestion.streaming.models import PriceEvent
from ingestion.streaming.s3_event_writer import S3PriceEventWriter


class KinesisToS3PriceEventConsumer:
    def __init__(
        self,
        *,
        stream_name: str,
        kinesis_client: Any,
        s3_writer: S3PriceEventWriter,
    ) -> None:
        self.stream_name = stream_name
        self.kinesis_client = kinesis_client
        self.s3_writer = s3_writer

    def consume_once(self, *, shard_iterator: str, limit: int = 100) -> list[str]:
        response = self.kinesis_client.get_records(
            ShardIterator=shard_iterator,
            Limit=limit,
        )

        written_paths: list[str] = []

        for record in response.get("Records", []):
            payload = json.loads(record["Data"].decode("utf-8"))
            event = PriceEvent.model_validate(payload)
            written_paths.append(self.s3_writer.write(event))

        return written_paths
