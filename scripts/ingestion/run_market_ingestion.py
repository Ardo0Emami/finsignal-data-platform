from __future__ import annotations

from typing import Any

from app.core.config import Settings
from ingestion.audit.local_writer import LocalAuditWriter
from ingestion.audit.models import IngestionAuditEvent
from ingestion.providers.base import MarketDataProvider
from ingestion.providers.static_sample import StaticSampleProvider
from ingestion.services.market_ingestion_service import (
    MarketIngestionService,
    build_failure_audit_event,
    build_success_audit_event,
)
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


def build_ingestion_service(settings: Settings | None = None) -> MarketIngestionService:
    settings = settings or Settings()

    return MarketIngestionService(
        provider=build_provider(settings),
        writer=build_writer(settings),
        audit_writer=LocalAuditWriter(settings.local_raw_base_path),
    )


def run_full_pipeline(settings: Settings | None = None) -> list[dict[str, Any]]:
    """Run the configured market ingestion pipeline.

    This is the clean callable entrypoint for Airflow.
    Airflow should call this function instead of duplicating ingestion logic.
    """

    settings = settings or Settings()
    symbols = parse_asset_symbols(settings)
    service = build_ingestion_service(settings)
    results = service.run_for_symbols(symbols)

    return [
        {
            "symbol": result.symbol,
            "status": result.status,
            "records_extracted": result.records_extracted,
            "records_written": result.records_written,
            "raw_path": result.raw_path,
            "audit_path": result.audit_path,
            "error_message": result.error_message,
        }
        for result in results
    ]


def _print_result(result: dict[str, Any]) -> None:
    if result["status"] == "succeeded":
        print(
            f"{result['symbol']}: wrote {result['records_written']} records "
            f"to {result['raw_path']}"
        )
        print(f"{result['symbol']}: wrote audit event to {result['audit_path']}")
        return

    print(f"{result['symbol']}: ingestion failed")
    print(f"{result['symbol']}: wrote failure audit event to {result['audit_path']}")


def main() -> None:
    results = run_full_pipeline()

    for result in results:
        _print_result(result)

        if result["status"] == "failed":
            raise RuntimeError(result["error_message"])


__all__ = [
    "IngestionAuditEvent",
    "build_failure_audit_event",
    "build_ingestion_service",
    "build_provider",
    "build_success_audit_event",
    "build_writer",
    "main",
    "parse_asset_symbols",
    "run_full_pipeline",
]


if __name__ == "__main__":
    main()
