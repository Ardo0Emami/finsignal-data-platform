from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ingestion.streaming.models import PriceEvent, RawPriceEventRow


def load_raw_price_event_row_from_file(path: Path) -> RawPriceEventRow:
    payload = json.loads(path.read_text(encoding="utf-8"))
    event = PriceEvent.model_validate(payload)

    return RawPriceEventRow(
        event_id=event.event_id,
        event_type=event.event_type,
        provider_name=event.provider_name,
        symbol=event.symbol,
        price_timestamp=event.price_timestamp,
        close_price=event.close_price,
        raw_path=str(path),
        ingested_at=event.ingested_at,
        raw_event=event.raw_event,
    )


def raw_price_event_row_to_snowflake_json(row: RawPriceEventRow) -> dict[str, Any]:
    return {
        "event_id": row.event_id,
        "event_type": row.event_type,
        "provider_name": row.provider_name,
        "symbol": row.symbol,
        "price_timestamp": row.price_timestamp.isoformat(),
        "close_price": row.close_price,
        "raw_path": row.raw_path,
        "ingested_at": row.ingested_at.isoformat(),
        "raw_event": row.raw_event,
    }
