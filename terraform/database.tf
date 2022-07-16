// PostgreSQL database
resource "aws_db_instance" "postgres" {
  identifier = "${var.prefix}-${var.environment}-rds-postgres"
  count      = var.postgres_enabled ? 1 : 0

  allocated_storage = 20
  engine            = "postgres"
  engine_version    = "12.10"
  instance_class    = "db.t2.micro"

  db_name  = var.postgres_database
  username = var.postgres_user
  password = var.postgres_password

  vpc_security_group_ids = [aws_security_group.security_group_postgres[0].id]
  db_subnet_group_name   = aws_db_subnet_group.subnet_group_postgres[0].name
  skip_final_snapshot    = true
  multi_az               = false
  publicly_accessible    = true

  tags = merge(local.common_tags, { category = "database", resource = "postgres", service = "rds" })
}

// Redshift Data Warehouse cluster
resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier  = "${var.prefix}-${var.environment}-redshift-cluster"
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  number_of_nodes     = 1
  skip_final_snapshot = true

  database_name   = var.redshift_database
  master_username = var.redshift_user
  master_password = var.redshift_password

  vpc_security_group_ids    = [aws_security_group.security_group_redshift.id]
  cluster_subnet_group_name = aws_redshift_subnet_group.subnet_group_redshift.name
  iam_roles                 = [aws_iam_role.role_redshift.arn]

  tags = merge(local.common_tags, { category = "database", resource = "redshift" })
}
