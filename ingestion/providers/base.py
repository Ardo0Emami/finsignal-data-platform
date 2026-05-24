from abc import ABC, abstractmethod
from datetime import date
from typing import Sequence

from ingestion.providers.models import MarketPriceRecord


class MarketDataProvider(ABC):
    provider_name: str

    @abstractmethod
    def fetch_daily_prices(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Sequence[MarketPriceRecord]:
        raise NotImplementedError

    @abstractmethod
    def fetch_latest_price(self, symbol: str) -> MarketPriceRecord:
        raise NotImplementedError
