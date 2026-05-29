from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from ingestion.audit.models import IngestionAuditEvent


def test_ingestion_audit_event_accepts_success_event() -> None:
    started_at = datetime.now(timezone.utc)
    completed_at = datetime.now(timezone.utc)

    event = IngestionAuditEvent(
        run_id="run-123",
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        status="succeeded",
        started_at=started_at,
        completed_at=completed_at,
        records_extracted=3,
        records_written=3,
        raw_path="data/raw/provider=static_sample/dataset=daily_prices/symbol=BTCUSD/data.json",
    )

    assert event.run_id == "run-123"
    assert event.status == "succeeded"
    assert event.records_extracted == 3
    assert event.records_written == 3
    assert event.error_message is None


def test_ingestion_audit_event_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        IngestionAuditEvent(
            run_id="run-123",
            provider_name="static_sample",
            dataset_name="daily_prices",
            symbol="BTCUSD",
            status="done",
            started_at=datetime.now(timezone.utc),
        )
