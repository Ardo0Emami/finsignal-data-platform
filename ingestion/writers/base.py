from abc import ABC, abstractmethod


class RawMarketDataWriter(ABC):
    @abstractmethod
    def write_market_prices(
        self,
        provider_name: str,
        dataset_name: str,
        symbol: str,
        records: list[dict],
        run_id: str | None = None,
    ) -> str:
        raise NotImplementedError
