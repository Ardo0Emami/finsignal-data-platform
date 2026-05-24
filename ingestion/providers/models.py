from pydantic import BaseModel


class MarketPriceRecord(BaseModel):
    provider_name: str
    symbol: str
    price_timestamp: str
    open_price: float | None = None
    high_price: float | None = None
    low_price: float | None = None
    close_price: float
    adjusted_close_price: float | None = None
    volume: float | None = None
    raw_record: dict
