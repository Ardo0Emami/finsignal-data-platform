from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import boto3

from ingestion.streaming.kinesis_producer import KinesisPriceEventProducer
from ingestion.streaming.models import PriceEvent
from ingestion.streaming.s3_event_writer import S3PriceEventWriter


def _parse_price_timestamp(value: object) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)

    if not isinstance(value, str):
        raise ValueError("price_timestamp must be an ISO-8601 string when provided")

    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)

    return parsed


def build_price_event_from_lambda_event(event: dict[str, Any]) -> PriceEvent:
    provider_name = str(event.get("provider_name", "static_sample"))
    symbol = str(event["symbol"])
    close_price = float(event["close_price"])
    price_timestamp = _parse_price_timestamp(event.get("price_timestamp"))

    return PriceEvent.latest_price(
        provider_name=provider_name,
        symbol=symbol,
        close_price=close_price,
        price_timestamp=price_timestamp,
        raw_event=event,
    )


def handle_latest_price_event(
    *,
    event: dict[str, Any],
    kinesis_client: Any,
    s3_client: Any,
    stream_name: str,
    bucket_name: str,
) -> dict[str, Any]:
    price_event = build_price_event_from_lambda_event(event)

    producer = KinesisPriceEventProducer(
        stream_name=stream_name,
        client=kinesis_client,
    )
    s3_writer = S3PriceEventWriter(
        bucket_name=bucket_name,
        client=s3_client,
    )

    event_id = producer.publish(price_event)
    raw_s3_path = s3_writer.write(price_event)

    return {
        "event_id": event_id,
        "event_type": price_event.event_type,
        "symbol": price_event.symbol,
        "provider_name": price_event.provider_name,
        "raw_s3_path": raw_s3_path,
    }


def handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    stream_name = os.environ["KINESIS_STREAM_NAME"]
    bucket_name = os.environ["RAW_BUCKET_NAME"]

    result = handle_latest_price_event(
        event=event,
        kinesis_client=boto3.client("kinesis"),
        s3_client=boto3.client("s3"),
        stream_name=stream_name,
        bucket_name=bucket_name,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
