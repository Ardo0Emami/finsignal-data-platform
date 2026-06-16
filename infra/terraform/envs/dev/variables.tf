variable "aws_region" {
  description = "AWS region for the dev environment."
  type        = string
  default     = "ca-central-1"
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "finsignal"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "lambda_package_path" {
  description = "Path to the zipped latest price ingestion Lambda package."
  type        = string
  default     = "../../../build/lambda/latest_price_ingestion.zip"
}
