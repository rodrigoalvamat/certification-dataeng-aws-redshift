// Project global variables
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "prefix" {
  description = "Resources prefix"
  type        = string
  default     = "udacity-dw"
}

variable "bucket_names" {
  description = "S3 bucket names"
  type        = list(string)
  default = [
    "landing-zone",
    "bronze-layer",
    "silver-layer",
    "gold-layer",
    "scripts"
  ]
}

// Prefix configuration and project common tags
locals {
  prefix = var.prefix
  common_tags = {
    environment = var.environment
    project     = "udacity-dw"
  }
}

// Redshift sensitive information
variable "redshift_database" {
  description = "Redshift database name"
  type        = string
  sensitive   = true
}

variable "redshift_user" {
  description = "Redshift admin user name"
  type        = string
  sensitive   = true
}

variable "redshift_password" {
  description = "Redshift admin password"
  type        = string
  sensitive   = true
}
