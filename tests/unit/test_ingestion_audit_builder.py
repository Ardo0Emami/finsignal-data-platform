from datetime import datetime, timezone

from scripts.ingestion.run_market_ingestion import build_success_audit_event


def test_build_success_audit_event_creates_success_record() -> None:
    started_at = datetime.now(timezone.utc)

    event = build_success_audit_event(
        run_id="run-123",
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        started_at=started_at,
        records_extracted=3,
        records_written=3,
        raw_path="data/raw/provider=static_sample/data.json",
    )

    assert event.run_id == "run-123"
    assert event.provider_name == "static_sample"
    assert event.dataset_name == "daily_prices"
    assert event.symbol == "BTCUSD"
    assert event.status == "succeeded"
    assert event.started_at == started_at
    assert event.completed_at is not None
    assert event.records_extracted == 3
    assert event.records_written == 3
    assert event.raw_path == "data/raw/provider=static_sample/data.json"
    assert event.error_message is None
