import json
import os
from datetime import datetime, timezone
from pathlib import Path

from ingestion.audit.local_writer import LocalAuditWriter
from ingestion.audit.models import IngestionAuditEvent
from scripts.audit.inspect_ingestion_audit import (
    find_audit_files,
    format_audit_summary,
    load_audit_event,
)


def test_find_audit_files_returns_events_newest_first(tmp_path) -> None:
    writer = LocalAuditWriter(str(tmp_path))

    older_event = IngestionAuditEvent(
        run_id="older-run",
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="BTCUSD",
        status="succeeded",
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        records_extracted=3,
        records_written=3,
        raw_path="data/raw/older.json",
    )

    newer_event = IngestionAuditEvent(
        run_id="newer-run",
        provider_name="static_sample",
        dataset_name="daily_prices",
        symbol="QQQ",
        status="succeeded",
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        records_extracted=3,
        records_written=3,
        raw_path="data/raw/newer.json",
    )

    older_path = Path(writer.write_event(older_event))
    newer_path = Path(writer.write_event(newer_event))

    os.utime(older_path, (1000, 1000))
    os.utime(newer_path, (2000, 2000))

    audit_files = find_audit_files(str(tmp_path))

    assert audit_files[0].name == "newer-run.json"
    assert audit_files[1].name == "older-run.json"


def test_load_audit_event_reads_json_payload(tmp_path) -> None:
    path = tmp_path / "event.json"
    path.write_text(json.dumps({"run_id": "run-123"}), encoding="utf-8")

    event = load_audit_event(path)

    assert event["run_id"] == "run-123"


def test_format_audit_summary_for_success_event() -> None:
    summary = format_audit_summary(
        {
            "status": "succeeded",
            "symbol": "BTCUSD",
            "provider_name": "static_sample",
            "dataset_name": "daily_prices",
            "records_written": 3,
            "run_id": "run-123",
            "error_message": None,
        }
    )

    assert summary == (
        "SUCCEEDED | symbol=BTCUSD | provider=static_sample | "
        "dataset=daily_prices | records_written=3 | run_id=run-123"
    )


def test_format_audit_summary_for_failed_event() -> None:
    summary = format_audit_summary(
        {
            "status": "failed",
            "symbol": "BTCUSD",
            "provider_name": "static_sample",
            "dataset_name": "daily_prices",
            "records_written": 0,
            "run_id": "run-456",
            "error_message": "provider timeout",
        }
    )

    assert summary == (
        "FAILED | symbol=BTCUSD | provider=static_sample | "
        "dataset=daily_prices | records_written=0 | "
        "run_id=run-456 | error=provider timeout"
    )
