variable "project" {
  description = "Project name used for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "raw_bucket_arn" {
  description = "ARN of the raw S3 bucket."
  type        = string
}

variable "kinesis_stream_arn" {
  description = "ARN of the Kinesis price event stream."
  type        = string
}
