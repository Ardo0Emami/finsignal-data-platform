output "ingestion_role_name" {
  description = "Name of the ingestion IAM role."
  value       = aws_iam_role.ingestion_role.name
}

output "ingestion_role_arn" {
  description = "ARN of the ingestion IAM role."
  value       = aws_iam_role.ingestion_role.arn
}

output "raw_bucket_write_policy_arn" {
  description = "ARN of the raw bucket write IAM policy."
  value       = aws_iam_policy.raw_bucket_write_policy.arn
}

output "kinesis_price_events_policy_arn" {
  description = "ARN of the Kinesis price events IAM policy."
  value       = aws_iam_policy.kinesis_price_events_policy.arn
}

output "lambda_logging_policy_arn" {
  description = "ARN of the Lambda logging IAM policy."
  value       = aws_iam_policy.lambda_logging_policy.arn
}
