import json
from datetime import date
from pathlib import Path

from ingestion.providers.base import MarketDataProvider
from ingestion.providers.models import MarketPriceRecord


class StaticSampleProvider(MarketDataProvider):
    provider_name = "static_sample"

    def __init__(self, sample_path: str):
        self.sample_path = Path(sample_path)

    def fetch_daily_prices(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[MarketPriceRecord]:
        payload = json.loads(self.sample_path.read_text())
        records: list[MarketPriceRecord] = []

        for item in payload["records"]:
            if item["symbol"] != symbol:
                continue

            price_date = date.fromisoformat(item["price_timestamp"][:10])

            if start_date is not None and price_date < start_date:
                continue

            if end_date is not None and price_date > end_date:
                continue

            records.append(
                MarketPriceRecord(
                    provider_name=self.provider_name,
                    symbol=item["symbol"],
                    price_timestamp=item["price_timestamp"],
                    open_price=item.get("open_price"),
                    high_price=item.get("high_price"),
                    low_price=item.get("low_price"),
                    close_price=item["close_price"],
                    adjusted_close_price=item.get("adjusted_close_price"),
                    volume=item.get("volume"),
                    raw_record=item,
                )
            )

        return records

    def fetch_latest_price(self, symbol: str) -> MarketPriceRecord:
        records = self.fetch_daily_prices(symbol)

        if not records:
            raise ValueError(f"No sample records found for symbol={symbol}")

        return sorted(records, key=lambda record: record.price_timestamp)[-1]
