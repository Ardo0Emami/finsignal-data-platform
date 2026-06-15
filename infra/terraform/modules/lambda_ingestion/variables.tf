variable "project" {
  description = "Project name used for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "raw_bucket_name" {
  description = "Raw S3 bucket name where event JSON files are written."
  type        = string
}

variable "kinesis_stream_name" {
  description = "Kinesis stream name for price events."
  type        = string
}

variable "lambda_execution_role_arn" {
  description = "IAM role ARN used by the Lambda function."
  type        = string
}

variable "lambda_package_path" {
  description = "Path to the zipped Lambda deployment package."
  type        = string
}

variable "timeout_seconds" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 30
}
