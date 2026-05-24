output "raw_bucket_name" {
  description = "Name of the raw S3 bucket."
  value       = aws_s3_bucket.raw.bucket
}

output "raw_bucket_arn" {
  description = "ARN of the raw S3 bucket."
  value       = aws_s3_bucket.raw.arn
}
