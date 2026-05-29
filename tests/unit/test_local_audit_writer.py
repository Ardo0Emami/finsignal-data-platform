import json
from datetime import datetime, timezone

from ingestion.audit.local_writer import LocalAuditWriter
from ingestion.audit.models import IngestionAuditEvent


def test_local_audit_writer_writes_event_file(tmp_path) -> None:
    writer = LocalAuditWriter(str(tmp_path))

    event = IngestionAuditEvent(
        run_id="run-123",
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        status="succeeded",
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        records_extracted=3,
        records_written=3,
        raw_path="data/raw/provider=static_sample/data.json",
    )

    audit_path = writer.write_event(event)

    audit_file = (
        tmp_path
        / "audit"
        / "ingestion_events"
        / "dataset=daily_prices"
        / "symbol=BTCUSD"
        / "run-123.json"
    )

    assert audit_path == str(audit_file)
    assert audit_file.exists()

    payload = json.loads(audit_file.read_text(encoding="utf-8"))

    assert payload["run_id"] == "run-123"
    assert payload["provider_name"] == "static_sample"
    assert payload["dataset_name"] == "daily_prices"
    assert payload["symbol"] == "BTCUSD"
    assert payload["status"] == "succeeded"
    assert payload["records_extracted"] == 3
    assert payload["records_written"] == 3
