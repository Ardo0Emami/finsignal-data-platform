from __future__ import annotations

from datetime import datetime, timezone

from ingestion.streaming.models import PriceEvent
from ingestion.streaming.raw_price_event_loader import load_raw_price_event_row_from_file


def test_load_raw_price_event_row_from_file(tmp_path) -> None:
    event = PriceEvent.latest_price(
        provider_name="static_sample",
        symbol="BTCUSD",
        close_price=69000.0,
        price_timestamp=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )

    path = tmp_path / "event.json"
    path.write_text(event.model_dump_json(), encoding="utf-8")

    row = load_raw_price_event_row_from_file(path)

    assert row.event_id == event.event_id
    assert row.event_type == "PRICE_TICK"
    assert row.provider_name == "static_sample"
    assert row.symbol == "BTCUSD"
    assert row.close_price == 69000.0
    assert row.raw_s3_path == str(path)
    assert row.raw_event["symbol"] == "BTCUSD"
