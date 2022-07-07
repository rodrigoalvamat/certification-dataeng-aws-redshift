// Cluster VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.2.0"

  name = "${var.prefix}-${var.environment}-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["us-west-2a", "us-west-2b", "us-west-2c", "us-west-2d"]
  #azs              = ["us-east-1a", "us-east-1b", "us-east-1c", "us-east-1d", "us-east-1e", "us-east-1f"]
  
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets   = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  database_subnets = ["10.0.7.0/24", "10.0.8.0/24", "10.0.9.0/24"]

  create_database_subnet_group = true
  enable_nat_gateway           = true
  single_nat_gateway           = true
  enable_dns_hostnames         = true

  tags = merge(local.common_tags, { category = "network", resource = "vpc" })
}

// PostgreSQL subnet group
resource "aws_db_subnet_group" "subnet_group_postgres" {
  name       = "${var.prefix}-${var.environment}-subnet-group-postgres"
  count      = var.postgres_enabled ? 1 : 0
  subnet_ids = module.vpc.public_subnets

  tags = merge(local.common_tags, { category = "network", resource = "subnet-group", service = "postgres" })
}

// PostgreSQL security group
resource "aws_security_group" "security_group_postgres" {
  description = "Allow PostgreSQL inbound traffic"

  name   = "${var.prefix}-${var.environment}-security-group-postgres"
  count  = var.postgres_enabled ? 1 : 0
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "all"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(local.common_tags, { category = "network", resource = "security-group", service = "postgres" })
}

// Redshift subnet group
resource "aws_redshift_subnet_group" "subnet_group_redshift" {
  name       = "${var.prefix}-${var.environment}-subnet-group-redshift"
  subnet_ids = module.vpc.public_subnets

  tags = merge(local.common_tags, { category = "network", resource = "subnet-group", service = "redshift" })
}

// Redshift security group
resource "aws_security_group" "security_group_redshift" {
  description = "Allow Redshift inbound traffic"

  name   = "${var.prefix}-${var.environment}-security-group-redshift"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "all"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "all"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(local.common_tags, { category = "network", resource = "security-group", service = "redshift" })
}
