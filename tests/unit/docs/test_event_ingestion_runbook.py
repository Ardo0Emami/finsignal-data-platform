from __future__ import annotations

from pathlib import Path

RUNBOOK_PATH = Path("docs/operations/event-ingestion-runbook.md")


def test_event_ingestion_runbook_exists() -> None:
    assert RUNBOOK_PATH.exists()


def test_event_ingestion_runbook_documents_core_event_flow() -> None:
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "Latest price payload" in runbook
    assert "Lambda latest-price handler" in runbook
    assert "Kinesis price-events stream" in runbook
    assert "S3 raw event landing" in runbook
    assert "Snowflake RAW_PRICE_EVENTS" in runbook


def test_event_ingestion_runbook_documents_operational_checks() -> None:
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "Validation Checklist" in runbook
    assert "Lambda package exists" in runbook
    assert "environment variables" in runbook
    assert "IAM permissions" in runbook
    assert "No Terraform apply" in runbook


def test_event_ingestion_runbook_documents_recovery_steps() -> None:
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "Recovery Notes" in runbook
    assert "CloudWatch" in runbook
    assert "S3" in runbook
    assert "PriceEvent" in runbook
