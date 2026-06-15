resource "aws_lambda_function" "latest_price_ingestion" {
  function_name = "${var.project}-${var.environment}-latest-price-ingestion"
  role          = var.lambda_execution_role_arn
  handler       = "ingestion.lambda_handlers.latest_price_ingestion.handler"
  runtime       = "python3.11"
  filename      = var.lambda_package_path
  timeout       = var.timeout_seconds

  environment {
    variables = {
      RAW_BUCKET_NAME     = var.raw_bucket_name
      KINESIS_STREAM_NAME = var.kinesis_stream_name
    }
  }

  tags = {
    Name        = "${var.project}-${var.environment}-latest-price-ingestion"
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
