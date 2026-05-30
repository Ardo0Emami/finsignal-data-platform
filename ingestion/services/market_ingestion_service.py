from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ingestion.audit.local_writer import LocalAuditWriter
from ingestion.audit.models import IngestionAuditEvent
from ingestion.providers.base import MarketDataProvider
from ingestion.writers.base import RawMarketDataWriter

DEFAULT_MARKET_DATASET_NAME = "daily_prices"


@dataclass(frozen=True)
class MarketIngestionResult:
    symbol: str
    status: str
    records_extracted: int
    records_written: int
    raw_path: str | None
    audit_path: str
    audit_event: IngestionAuditEvent
    error_message: str | None = None


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


def build_failure_audit_event(
    run_id: str,
    provider_name: str,
    dataset_name: str,
    symbol: str,
    started_at: datetime,
    error: Exception,
) -> IngestionAuditEvent:
    return IngestionAuditEvent(
        run_id=run_id,
        provider_name=provider_name,
        dataset_name=dataset_name,
        symbol=symbol,
        status="failed",
        started_at=started_at,
        completed_at=datetime.now(timezone.utc),
        error_message=str(error),
    )


class MarketIngestionService:
    """Coordinates market data extraction, raw landing, and audit recording.

    This service contains reusable ingestion workflow logic.
    Script entrypoints and future Airflow DAGs should call this service instead
    of implementing ingestion logic themselves.
    """

    def __init__(
        self,
        provider: MarketDataProvider,
        writer: RawMarketDataWriter,
        audit_writer: LocalAuditWriter,
        dataset_name: str = DEFAULT_MARKET_DATASET_NAME,
    ) -> None:
        self.provider = provider
        self.writer = writer
        self.audit_writer = audit_writer
        self.dataset_name = dataset_name

    def run_for_symbols(self, symbols: list[str]) -> list[MarketIngestionResult]:
        results: list[MarketIngestionResult] = []

        for symbol in symbols:
            results.append(self.run_for_symbol(symbol))

        return results

    def run_for_symbol(self, symbol: str) -> MarketIngestionResult:
        run_id = str(uuid4())
        started_at = datetime.now(timezone.utc)

        try:
            records = list(self.provider.fetch_daily_prices(symbol))
            record_payloads = [self._record_to_dict(record) for record in records]

            raw_path = self.writer.write_market_prices(
                provider_name=self.provider.provider_name,
                dataset_name=self.dataset_name,
                symbol=symbol,
                records=record_payloads,
                run_id=run_id,
            )

            audit_event = build_success_audit_event(
                run_id=run_id,
                provider_name=self.provider.provider_name,
                dataset_name=self.dataset_name,
                symbol=symbol,
                started_at=started_at,
                records_extracted=len(records),
                records_written=len(record_payloads),
                raw_path=raw_path,
            )
            audit_path = self.audit_writer.write_event(audit_event)

            return MarketIngestionResult(
                symbol=symbol,
                status="succeeded",
                records_extracted=len(records),
                records_written=len(record_payloads),
                raw_path=raw_path,
                audit_path=audit_path,
                audit_event=audit_event,
            )

        except Exception as error:
            audit_event = build_failure_audit_event(
                run_id=run_id,
                provider_name=self.provider.provider_name,
                dataset_name=self.dataset_name,
                symbol=symbol,
                started_at=started_at,
                error=error,
            )
            audit_path = self.audit_writer.write_event(audit_event)

            return MarketIngestionResult(
                symbol=symbol,
                status="failed",
                records_extracted=0,
                records_written=0,
                raw_path=None,
                audit_path=audit_path,
                audit_event=audit_event,
                error_message=str(error),
            )

    def _record_to_dict(self, record: Any) -> dict[str, Any]:
        if hasattr(record, "model_dump"):
            return record.model_dump()

        if isinstance(record, dict):
            return record

        raise TypeError(f"Unsupported market price record type: {type(record)!r}")
