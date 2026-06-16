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

output "price_events_stream_name" {
  description = "Name of the Kinesis price events stream."
  value       = module.kinesis.stream_name
}

output "price_events_stream_arn" {
  description = "ARN of the Kinesis price events stream."
  value       = module.kinesis.stream_arn
}

output "latest_price_ingestion_lambda_name" {
  description = "Name of the latest price ingestion Lambda function."
  value       = module.lambda_ingestion.function_name
}

output "latest_price_ingestion_lambda_arn" {
  description = "ARN of the latest price ingestion Lambda function."
  value       = module.lambda_ingestion.function_arn
}
