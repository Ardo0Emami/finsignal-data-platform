from ingestion.providers.static_sample import StaticSampleProvider
from ingestion.writers.local_writer import LocalRawWriter

ASSET_UNIVERSE = ["BTCUSD", "QQQ"]
SAMPLE_DATA_PATH = "data_samples/market_prices_sample.json"
LOCAL_RAW_BASE_PATH = "data"


def main() -> None:
    provider = StaticSampleProvider(SAMPLE_DATA_PATH)
    writer = LocalRawWriter(LOCAL_RAW_BASE_PATH)

    for symbol in ASSET_UNIVERSE:
        records = provider.fetch_daily_prices(symbol)

        raw_path = writer.write_market_prices(
            provider_name=provider.provider_name,
            dataset_name="daily_prices",
            symbol=symbol,
            records=[record.model_dump() for record in records],
        )

        print(f"{symbol}: wrote {len(records)} records to {raw_path}")


if __name__ == "__main__":
    main()
