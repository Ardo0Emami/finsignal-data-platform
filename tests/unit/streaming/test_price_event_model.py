from __future__ import annotations

from datetime import datetime, timezone

from ingestion.streaming.models import PriceEvent


def test_latest_price_event_normalizes_symbol_and_preserves_raw_event() -> None:
    event = PriceEvent.latest_price(
        provider_name="static_sample",
        symbol="btcusd",
        close_price=69000.0,
        price_timestamp=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )

    assert event.event_type == "PRICE_TICK"
    assert event.provider_name == "static_sample"
    assert event.symbol == "BTCUSD"
    assert event.close_price == 69000.0
    assert event.raw_event["symbol"] == "BTCUSD"
    assert event.event_id
