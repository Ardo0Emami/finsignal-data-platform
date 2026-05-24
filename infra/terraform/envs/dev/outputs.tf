output "raw_bucket_name" {
  description = "Name of the raw S3 bucket."
  value       = module.storage.raw_bucket_name
}

output "raw_bucket_arn" {
  description = "ARN of the raw S3 bucket."
  value       = module.storage.raw_bucket_arn
}
