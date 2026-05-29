from datetime import datetime, timezone

from scripts.ingestion.run_market_ingestion import build_failure_audit_event


def test_build_failure_audit_event_creates_failed_record() -> None:
    started_at = datetime.now(timezone.utc)
    error = RuntimeError("provider timeout")

    event = build_failure_audit_event(
        run_id="run-456",
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        started_at=started_at,
        error=error,
    )

    assert event.run_id == "run-456"
    assert event.provider_name == "static_sample"
    assert event.dataset_name == "daily_prices"
    assert event.symbol == "BTCUSD"
    assert event.status == "failed"
    assert event.started_at == started_at
    assert event.completed_at is not None
    assert event.records_extracted == 0
    assert event.records_written == 0
    assert event.raw_path is None
    assert event.error_message == "provider timeout"
