from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class PriceEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str = "PRICE_TICK"
    provider_name: str
    symbol: str
    price_timestamp: datetime
    close_price: float
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_event: dict[str, Any]

    @classmethod
    def latest_price(
        cls,
        *,
        provider_name: str,
        symbol: str,
        close_price: float,
        price_timestamp: datetime | None = None,
        raw_event: dict[str, Any] | None = None,
    ) -> PriceEvent:
        timestamp = price_timestamp or datetime.now(timezone.utc)

        return cls(
            provider_name=provider_name,
            symbol=symbol.upper(),
            price_timestamp=timestamp,
            close_price=close_price,
            raw_event=raw_event
            or {
                "provider_name": provider_name,
                "symbol": symbol.upper(),
                "close_price": close_price,
                "price_timestamp": timestamp.isoformat(),
            },
        )


class RawPriceEventRow(BaseModel):
    event_id: str
    event_type: str
    provider_name: str
    symbol: str
    price_timestamp: datetime
    close_price: float
    raw_s3_path: str
    ingested_at: datetime
    raw_event: dict[str, Any]
