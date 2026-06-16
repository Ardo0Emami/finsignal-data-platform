from __future__ import annotations

from pathlib import Path


def test_dev_environment_wires_storage_kinesis_iam_and_lambda_modules() -> None:
    main = Path("infra/terraform/envs/dev/main.tf").read_text(encoding="utf-8")

    assert 'module "storage"' in main
    assert 'module "kinesis"' in main
    assert 'module "iam"' in main
    assert 'module "lambda_ingestion"' in main
    assert "raw_bucket_arn     = module.storage.raw_bucket_arn" in main
    assert "kinesis_stream_arn = module.kinesis.stream_arn" in main
    assert "raw_bucket_name           = module.storage.raw_bucket_name" in main
    assert "kinesis_stream_name       = module.kinesis.stream_name" in main
    assert "lambda_execution_role_arn = module.iam.ingestion_role_arn" in main


def test_dev_environment_outputs_event_ingestion_resources() -> None:
    outputs = Path("infra/terraform/envs/dev/outputs.tf").read_text(encoding="utf-8")

    assert "price_events_stream_name" in outputs
    assert "price_events_stream_arn" in outputs
    assert "latest_price_ingestion_lambda_name" in outputs
    assert "latest_price_ingestion_lambda_arn" in outputs


def test_iam_module_grants_s3_kinesis_and_lambda_logging_permissions() -> None:
    main = Path("infra/terraform/modules/iam/main.tf").read_text(encoding="utf-8")
    variables = Path("infra/terraform/modules/iam/variables.tf").read_text(
        encoding="utf-8"
    )

    assert "kinesis_stream_arn" in variables
    assert 'resource "aws_iam_policy" "raw_bucket_write_policy"' in main
    assert 'resource "aws_iam_policy" "kinesis_price_events_policy"' in main
    assert 'resource "aws_iam_policy" "lambda_logging_policy"' in main
    assert "kinesis:PutRecord" in main
    assert "kinesis:GetRecords" in main
    assert "logs:PutLogEvents" in main
    assert "s3:PutObject" in main
