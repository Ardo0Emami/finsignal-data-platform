from __future__ import annotations

from pathlib import Path


def test_dev_environment_has_lambda_package_variable() -> None:
    variables = Path("infra/terraform/envs/dev/variables.tf").read_text(
        encoding="utf-8"
    )

    assert "lambda_package_path" in variables
    assert "../../../build/lambda/latest_price_ingestion.zip" in variables


def test_lambda_ingestion_module_uses_packaged_handler_path() -> None:
    main = Path("infra/terraform/modules/lambda_ingestion/main.tf").read_text(
        encoding="utf-8"
    )

    assert 'handler       = "ingestion.lambda_handlers.latest_price_ingestion.handler"' in main
    assert 'runtime       = "python3.11"' in main
    assert "filename      = var.lambda_package_path" in main


def test_event_ingestion_dev_environment_does_not_define_apply_only_resources() -> None:
    main = Path("infra/terraform/envs/dev/main.tf").read_text(encoding="utf-8")

    assert 'module "kinesis"' in main
    assert 'module "lambda_ingestion"' in main
    assert "aws_lambda_function" not in main
    assert "aws_kinesis_stream" not in main
