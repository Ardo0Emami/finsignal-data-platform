output "raw_bucket_name" {
  description = "Name of the raw S3 bucket."
  value       = module.storage.raw_bucket_name
}

output "raw_bucket_arn" {
  description = "ARN of the raw S3 bucket."
  value       = module.storage.raw_bucket_arn
}

output "ingestion_role_name" {
  description = "Name of the ingestion IAM role."
  value       = module.iam.ingestion_role_name
}

output "ingestion_role_arn" {
  description = "ARN of the ingestion IAM role."
  value       = module.iam.ingestion_role_arn
}
