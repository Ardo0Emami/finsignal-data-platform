from app.core.config import Settings
from ingestion.providers.static_sample import StaticSampleProvider
from ingestion.writers.local_writer import LocalRawWriter
from ingestion.writers.s3_writer import S3RawWriter

ASSET_UNIVERSE = ["BTCUSD", "QQQ"]


def build_writer(settings: Settings | None = None):
    settings = settings or Settings()
    writer_type = settings.raw_writer.lower().strip()

    if writer_type == "local":
        return LocalRawWriter(settings.local_raw_base_path)

    if writer_type == "s3":
        if not settings.raw_bucket:
            raise ValueError(
                "FINSIGNAL_RAW_BUCKET must be set when FINSIGNAL_RAW_WRITER=s3"
            )

        return S3RawWriter(bucket_name=settings.raw_bucket)

    raise ValueError(
        f"Unsupported FINSIGNAL_RAW_WRITER={writer_type}. Expected 'local' or 's3'."
    )


def main() -> None:
    settings = Settings()
    provider = StaticSampleProvider(settings.sample_data_path)
    writer = build_writer(settings)

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
