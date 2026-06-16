terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

module "storage" {
  source      = "../../modules/storage"
  project     = var.project_name
  environment = var.environment
}

module "kinesis" {
  source      = "../../modules/kinesis"
  project     = var.project_name
  environment = var.environment
}

module "iam" {
  source             = "../../modules/iam"
  project            = var.project_name
  environment        = var.environment
  raw_bucket_arn     = module.storage.raw_bucket_arn
  kinesis_stream_arn = module.kinesis.stream_arn
}

module "lambda_ingestion" {
  source                    = "../../modules/lambda_ingestion"
  project                   = var.project_name
  environment               = var.environment
  raw_bucket_name           = module.storage.raw_bucket_name
  kinesis_stream_name       = module.kinesis.stream_name
  lambda_execution_role_arn = module.iam.ingestion_role_arn
  lambda_package_path       = var.lambda_package_path
}
