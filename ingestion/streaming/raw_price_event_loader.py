from __future__ import annotations

import json
from pathlib import Path

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
        raw_s3_path=str(path),
        ingested_at=event.ingested_at,
        raw_event=event.raw_event,
    )
