import os

from ingestion.providers.static_sample import StaticSampleProvider
from ingestion.writers.local_writer import LocalRawWriter
from ingestion.writers.s3_writer import S3RawWriter

ASSET_UNIVERSE = ["BTCUSD", "QQQ"]
SAMPLE_DATA_PATH = "data_samples/market_prices_sample.json"
LOCAL_RAW_BASE_PATH = "data"


def build_writer():
    writer_type = os.getenv("FINSIGNAL_RAW_WRITER", "local").lower().strip()

    if writer_type == "local":
        return LocalRawWriter(LOCAL_RAW_BASE_PATH)

    if writer_type == "s3":
        bucket_name = os.getenv("FINSIGNAL_RAW_BUCKET")
        if not bucket_name:
            raise ValueError(
                "FINSIGNAL_RAW_BUCKET must be set when FINSIGNAL_RAW_WRITER=s3"
            )

        return S3RawWriter(bucket_name=bucket_name)

    raise ValueError(
        f"Unsupported FINSIGNAL_RAW_WRITER={writer_type}. Expected 'local' or 's3'."
    )


def main() -> None:
    provider = StaticSampleProvider(SAMPLE_DATA_PATH)
    writer = build_writer()

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
