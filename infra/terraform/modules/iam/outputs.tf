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
