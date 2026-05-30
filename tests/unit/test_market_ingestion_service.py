from __future__ import annotations

from datetime import date
from typing import Any

from ingestion.audit.models import IngestionAuditEvent
from ingestion.services.market_ingestion_service import MarketIngestionService


class FakeProvider:
    provider_name = "fake_provider"

    def fetch_daily_prices(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[dict[str, Any]]:
        return [
            {
                "provider_name": self.provider_name,
                "symbol": symbol,
                "price_timestamp": "2026-05-22T00:00:00Z",
                "close_price": 100.0,
                "raw_record": {"symbol": symbol, "close": 100.0},
            }
        ]

    def fetch_latest_price(self, symbol: str) -> dict[str, Any]:
        return {
            "provider_name": self.provider_name,
            "symbol": symbol,
            "price_timestamp": "2026-05-22T00:00:00Z",
            "close_price": 100.0,
            "raw_record": {"symbol": symbol, "close": 100.0},
        }


class FailingProvider:
    provider_name = "failing_provider"

    def fetch_daily_prices(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[dict[str, Any]]:
        raise RuntimeError(f"provider failed for {symbol}")

    def fetch_latest_price(self, symbol: str) -> dict[str, Any]:
        raise RuntimeError(f"provider failed for {symbol}")


class FakeRawWriter:
    def __init__(self) -> None:
        self.written_records: list[dict[str, Any]] = []

    def write_market_prices(
        self,
        provider_name: str,
        dataset_name: str,
        symbol: str,
        records: list[dict[str, Any]],
        run_id: str | None = None,
    ) -> str:
        self.written_records.extend(records)
        return (
            f"local://raw/provider={provider_name}/dataset={dataset_name}/"
            f"symbol={symbol}/run_id={run_id}/data.json"
        )


class FakeAuditWriter:
    def __init__(self) -> None:
        self.events: list[IngestionAuditEvent] = []

    def write_event(self, event: IngestionAuditEvent) -> str:
        self.events.append(event)
        return f"local://audit/{event.run_id}.json"


def test_market_ingestion_service_writes_raw_data_and_success_audit() -> None:
    raw_writer = FakeRawWriter()
    audit_writer = FakeAuditWriter()

    service = MarketIngestionService(
        provider=FakeProvider(),
        writer=raw_writer,
        audit_writer=audit_writer,
    )

    result = service.run_for_symbol("BTCUSD")

    assert result.symbol == "BTCUSD"
    assert result.status == "succeeded"
    assert result.records_extracted == 1
    assert result.records_written == 1
    assert result.raw_path is not None
    assert result.audit_path.startswith("local://audit/")
    assert result.error_message is None

    assert len(raw_writer.written_records) == 1
    assert raw_writer.written_records[0]["symbol"] == "BTCUSD"

    assert len(audit_writer.events) == 1
    assert audit_writer.events[0].status == "succeeded"
    assert audit_writer.events[0].symbol == "BTCUSD"
    assert audit_writer.events[0].records_extracted == 1
    assert audit_writer.events[0].records_written == 1


def test_market_ingestion_service_records_failure_audit() -> None:
    raw_writer = FakeRawWriter()
    audit_writer = FakeAuditWriter()

    service = MarketIngestionService(
        provider=FailingProvider(),
        writer=raw_writer,
        audit_writer=audit_writer,
    )

    result = service.run_for_symbol("QQQ")

    assert result.symbol == "QQQ"
    assert result.status == "failed"
    assert result.records_extracted == 0
    assert result.records_written == 0
    assert result.raw_path is None
    assert result.audit_path.startswith("local://audit/")
    assert result.error_message == "provider failed for QQQ"

    assert raw_writer.written_records == []

    assert len(audit_writer.events) == 1
    assert audit_writer.events[0].status == "failed"
    assert audit_writer.events[0].symbol == "QQQ"
    assert audit_writer.events[0].error_message == "provider failed for QQQ"
