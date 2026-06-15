variable "project" {
  description = "Project name used for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "shard_count" {
  description = "Number of Kinesis shards for the price event stream."
  type        = number
  default     = 1
}

variable "retention_period_hours" {
  description = "Retention period for Kinesis records in hours."
  type        = number
  default     = 24
}
