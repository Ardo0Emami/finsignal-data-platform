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

module "iam" {
  source         = "../../modules/iam"
  project        = var.project_name
  environment    = var.environment
  raw_bucket_arn = module.storage.raw_bucket_arn
}
