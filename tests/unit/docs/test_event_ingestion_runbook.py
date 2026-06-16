from __future__ import annotations

from pathlib import Path

RUNBOOK_PATH = Path("docs/operations/event-ingestion-runbook.md")


def _read_runbook() -> str:
    return RUNBOOK_PATH.read_text(encoding="utf-8")


def test_event_ingestion_runbook_documents_architecture_and_components() -> None:
    runbook = _read_runbook()

    assert "# Event Ingestion Runbook" in runbook
    assert "Lambda latest-price handler" in runbook
    assert "Kinesis price-events stream" in runbook
    assert "S3 raw event landing" in runbook
    assert "Snowflake RAW_PRICE_EVENTS" in runbook
    assert "ingestion/lambda_handlers/latest_price_ingestion.py" in runbook
    assert "ingestion/streaming/models.py" in runbook
    assert "ingestion/streaming/kinesis_producer.py" in runbook
    assert "ingestion/streaming/s3_event_writer.py" in runbook
    assert "ingestion/streaming/kinesis_consumer.py" in runbook


def test_event_ingestion_runbook_documents_raw_event_contract() -> None:
    runbook = _read_runbook()

    assert "## Raw Event Contract" in runbook
    assert "event_id" in runbook
    assert "event_type" in runbook
    assert "provider_name" in runbook
    assert "symbol" in runbook
    assert "price_timestamp" in runbook
    assert "close_price" in runbook
    assert "ingested_at" in runbook
    assert "raw_event" in runbook
    assert "FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS" in runbook


def test_event_ingestion_runbook_documents_raw_landing_path() -> None:
    runbook = _read_runbook()

    assert "## Raw Landing Path" in runbook
    assert "events/event_type=PRICE_TICK" in runbook
    assert "symbol=<SYMBOL>" in runbook
    assert "ingestion_date=<DATE>" in runbook
    assert "event_id=<EVENT_ID>.json" in runbook
    assert "traceable, replayable" in runbook


def test_event_ingestion_runbook_documents_local_validation() -> None:
    runbook = _read_runbook()

    assert "## Local Validation" in runbook
    assert "python -m ruff check ." in runbook
    assert "python -m pytest" in runbook
    assert "python -m scripts.lambda_tools.package_latest_price_ingestion" in runbook
    assert "python -m scripts.snowflake.create_sample_price_event_file" in runbook
    assert "python -m scripts.snowflake.load_raw_price_events" in runbook
    assert ".local/price_events/sample_btc_event.json" in runbook


def test_event_ingestion_runbook_documents_snowflake_inspection_query() -> None:
    runbook = _read_runbook()

    assert "SELECT" in runbook
    assert "event_id" in runbook
    assert "event_type" in runbook
    assert "provider_name" in runbook
    assert "raw_path" in runbook
    assert "FROM FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS" in runbook
    assert "ORDER BY ingested_at DESC" in runbook
    assert "LIMIT 5" in runbook


def test_event_ingestion_runbook_documents_terraform_validation() -> None:
    runbook = _read_runbook()

    assert "## Terraform Validation" in runbook
    assert "terraform init" in runbook
    assert "terraform fmt -check -recursive ../.." in runbook
    assert "terraform validate" in runbook
    assert "build/lambda/latest_price_ingestion.zip" in runbook


def test_event_ingestion_runbook_documents_aws_deployment_notes() -> None:
    runbook = _read_runbook()

    assert "## AWS Deployment Notes" in runbook
    assert "Do not run `terraform apply`" in runbook
    assert "terraform plan" in runbook
    assert "terraform apply" in runbook
    assert "terraform destroy" in runbook


def test_event_ingestion_runbook_documents_cost_guardrails() -> None:
    runbook = _read_runbook()

    assert "## Cost Guardrails" in runbook
    assert "Kinesis uses one provisioned shard in dev" in runbook
    assert "Lambda is event-driven" in runbook
    assert "Snowflake warehouse must remain auto-suspended" in runbook
    assert "Do not run Terraform apply casually during local development" in runbook


def test_event_ingestion_runbook_documents_validation_checklist() -> None:
    runbook = _read_runbook()

    assert "## Validation Checklist" in runbook
    assert "Lambda package exists" in runbook
    assert "Lambda environment variables are configured" in runbook
    assert "Kinesis stream name matches the deployed stream" in runbook
    assert "S3 raw bucket exists" in runbook
    assert "IAM permissions allow Lambda, Kinesis, S3, and CloudWatch Logs operations" in runbook
    assert "Terraform validate succeeds" in runbook


def test_event_ingestion_runbook_documents_recovery_notes() -> None:
    runbook = _read_runbook()

    assert "## Recovery Notes" in runbook
    assert "Check Lambda logs in CloudWatch" in runbook
    assert "Confirm required environment variables are present" in runbook
    assert "Verify Kinesis stream name and permissions" in runbook
    assert "Check whether raw event files were written to S3" in runbook
    assert "Validate event payload shape against the `PriceEvent` model" in runbook
    assert "Reprocess raw event files after the root cause is fixed" in runbook


def test_event_ingestion_runbook_documents_done_criteria() -> None:
    runbook = _read_runbook()

    assert "## Done Criteria" in runbook
    assert "A latest-price event can be created" in runbook
    assert "The event can be published through the event-ingestion abstraction" in runbook
    assert "The event can land as raw JSON" in runbook
    assert "The event can be loaded into FINSIGNAL_DW.RAW.RAW_PRICE_EVENTS" in runbook
    assert "Terraform defines the AWS Kinesis/Lambda/IAM path" in runbook
    assert "The Lambda package can be built" in runbook


def test_event_ingestion_runbook_documents_public_explanation() -> None:
    runbook = _read_runbook()

    assert "## Public Explanation" in runbook
    assert "FinSignal supports both batch and event-style ingestion" in runbook
    assert "Batch ingestion handles scheduled historical and daily market data" in runbook
    assert "Event ingestion handles lightweight latest-price snapshots" in runbook