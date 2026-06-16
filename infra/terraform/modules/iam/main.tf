resource "aws_iam_role" "ingestion_role" {
  name = "${var.project}-${var.environment}-ingestion-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "raw_bucket_write_policy" {
  name        = "${var.project}-${var.environment}-raw-bucket-write-policy"
  description = "Allows ingestion workloads to write raw market data files to the FinSignal raw bucket."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.raw_bucket_arn,
          "${var.raw_bucket_arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "kinesis_price_events_policy" {
  name        = "${var.project}-${var.environment}-kinesis-price-events-policy"
  description = "Allows ingestion workloads to publish and consume FinSignal price events."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "kinesis:PutRecord",
          "kinesis:PutRecords",
          "kinesis:DescribeStream",
          "kinesis:GetShardIterator",
          "kinesis:GetRecords"
        ]
        Resource = var.kinesis_stream_arn
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_logging_policy" {
  name        = "${var.project}-${var.environment}-lambda-logging-policy"
  description = "Allows Lambda ingestion workloads to write CloudWatch logs."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "raw_bucket_write_attachment" {
  role       = aws_iam_role.ingestion_role.name
  policy_arn = aws_iam_policy.raw_bucket_write_policy.arn
}

resource "aws_iam_role_policy_attachment" "kinesis_price_events_attachment" {
  role       = aws_iam_role.ingestion_role.name
  policy_arn = aws_iam_policy.kinesis_price_events_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_logging_attachment" {
  role       = aws_iam_role.ingestion_role.name
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
}
