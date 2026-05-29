from datetime import datetime, timezone
from uuid import uuid4

from app.core.config import Settings
from ingestion.audit.local_writer import LocalAuditWriter
from ingestion.audit.models import IngestionAuditEvent
from ingestion.providers.base import MarketDataProvider
from ingestion.providers.static_sample import StaticSampleProvider
from ingestion.writers.base import RawMarketDataWriter
from ingestion.writers.local_writer import LocalRawWriter
from ingestion.writers.s3_writer import S3RawWriter


def parse_asset_symbols(settings: Settings) -> list[str]:
    symbols = [
        symbol.strip().upper()
        for symbol in settings.asset_symbols.split(",")
        if symbol.strip()
    ]

    if not symbols:
        raise ValueError("FINSIGNAL_ASSET_SYMBOLS must include at least one symbol.")

    return symbols


def build_provider(settings: Settings | None = None) -> MarketDataProvider:
    settings = settings or Settings()
    provider_type = settings.market_data_provider.lower().strip()

    if provider_type == "static_sample":
        return StaticSampleProvider(settings.sample_data_path)

    raise ValueError(
        "Unsupported FINSIGNAL_MARKET_DATA_PROVIDER="
        f"{provider_type}. Expected 'static_sample'."
    )


def build_writer(settings: Settings | None = None) -> RawMarketDataWriter:
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


def build_success_audit_event(
    run_id: str,
    provider_name: str,
    dataset_name: str,
    symbol: str,
    started_at: datetime,
    records_extracted: int,
    records_written: int,
    raw_path: str,
) -> IngestionAuditEvent:
    return IngestionAuditEvent(
        run_id=run_id,
        provider_name=provider_name,
        dataset_name=dataset_name,
        symbol=symbol,
        status="succeeded",
        started_at=started_at,
        completed_at=datetime.now(timezone.utc),
        records_extracted=records_extracted,
        records_written=records_written,
        raw_path=raw_path,
    )


def main() -> None:
    settings = Settings()
    provider = build_provider(settings)
    writer = build_writer(settings)
    audit_writer = LocalAuditWriter(settings.local_raw_base_path)
    asset_symbols = parse_asset_symbols(settings)

    for symbol in asset_symbols:
        started_at = datetime.now(timezone.utc)
        run_id = str(uuid4())

        records = provider.fetch_daily_prices(symbol)

        raw_path = writer.write_market_prices(
            provider_name=provider.provider_name,
            dataset_name="daily_prices",
            symbol=symbol,
            records=[record.model_dump() for record in records],
            run_id=run_id,
        )

        audit_event = build_success_audit_event(
            run_id=run_id,
            provider_name=provider.provider_name,
            dataset_name="daily_prices",
            symbol=symbol,
            started_at=started_at,
            records_extracted=len(records),
            records_written=len(records),
            raw_path=raw_path,
        )

        audit_path = audit_writer.write_event(audit_event)

        print(f"{symbol}: wrote {len(records)} records to {raw_path}")
        print(f"{symbol}: wrote audit event to {audit_path}")
        print(audit_event.model_dump_json())


if __name__ == "__main__":
    main()
