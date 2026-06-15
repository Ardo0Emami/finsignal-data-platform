from __future__ import annotations

from pathlib import Path


def test_kinesis_module_defines_price_event_stream_with_cost_guardrails() -> None:
    main = Path("infra/terraform/modules/kinesis/main.tf").read_text(
        encoding="utf-8"
    )
    variables = Path("infra/terraform/modules/kinesis/variables.tf").read_text(
        encoding="utf-8"
    )
    outputs = Path("infra/terraform/modules/kinesis/outputs.tf").read_text(
        encoding="utf-8"
    )

    assert 'resource "aws_kinesis_stream" "price_events"' in main
    assert '"${var.project}-${var.environment}-price-events"' in main
    assert "stream_mode = \"PROVISIONED\"" in main
    assert "shard_count      = var.shard_count" in main
    assert "default     = 1" in variables
    assert "retention_period_hours" in variables
    assert "stream_name" in outputs
    assert "stream_arn" in outputs


def test_lambda_ingestion_module_defines_latest_price_lambda() -> None:
    main = Path("infra/terraform/modules/lambda_ingestion/main.tf").read_text(
        encoding="utf-8"
    )
    variables = Path(
        "infra/terraform/modules/lambda_ingestion/variables.tf"
    ).read_text(encoding="utf-8")
    outputs = Path("infra/terraform/modules/lambda_ingestion/outputs.tf").read_text(
        encoding="utf-8"
    )

    assert 'resource "aws_lambda_function" "latest_price_ingestion"' in main
    assert '"${var.project}-${var.environment}-latest-price-ingestion"' in main
    assert 'runtime       = "python3.11"' in main
    assert "ingestion.lambda_handlers.latest_price_ingestion.handler" in main
    assert "RAW_BUCKET_NAME" in main
    assert "KINESIS_STREAM_NAME" in main
    assert "lambda_execution_role_arn" in variables
    assert "lambda_package_path" in variables
    assert "function_name" in outputs
    assert "function_arn" in outputs
