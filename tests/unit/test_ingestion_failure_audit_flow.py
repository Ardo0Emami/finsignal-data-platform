from pathlib import Path

import pytest

from app.core.config import Settings
from ingestion.providers.models import MarketPriceRecord
from ingestion.writers.local_writer import LocalRawWriter
from scripts.ingestion import run_market_ingestion


class FailingProvider:
    provider_name = "failing_provider"

    def fetch_daily_prices(
        self,
        symbol: str,
        start_date=None,
        end_date=None,
    ) -> list[MarketPriceRecord]:
        raise RuntimeError("simulated provider failure")

    def fetch_latest_price(self, symbol: str) -> MarketPriceRecord:
        raise RuntimeError("simulated provider failure")


def test_main_writes_failure_audit_event_when_symbol_ingestion_fails(
    monkeypatch,
    tmp_path,
) -> None:
    settings = Settings(
        raw_writer="local",
        local_raw_base_path=str(tmp_path),
        asset_symbols="BTCUSD",
    )

    monkeypatch.setattr(run_market_ingestion, "Settings", lambda: settings)
    monkeypatch.setattr(
        run_market_ingestion,
        "build_provider",
        lambda settings: FailingProvider(),
    )
    monkeypatch.setattr(
        run_market_ingestion,
        "build_writer",
        lambda settings: LocalRawWriter(settings.local_raw_base_path),
    )

    with pytest.raises(RuntimeError, match="simulated provider failure"):
        run_market_ingestion.main()

    audit_files = list(Path(tmp_path).glob("audit/ingestion_events/**/*.json"))

    assert len(audit_files) == 1
    assert "symbol=BTCUSD" in str(audit_files[0])

    payload = audit_files[0].read_text(encoding="utf-8")

    assert '"status": "failed"' in payload
    assert '"error_message": "simulated provider failure"' in payload
