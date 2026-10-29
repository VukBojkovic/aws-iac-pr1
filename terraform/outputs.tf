output "vpc_id" {
  value       = aws_vpc.main.id
  description = "ID for created VPC"
}

output "public_subnet_ids" {
  value       = aws_subnet.public[*].id
  description = "ID for Public Subnets"
}

output "private_app_subnet_ids" {
  value       = aws_subnet.private_app[*].id
  description = "ID for Private App Subnets"
}

output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "DNS name of the Application Load Balancer"
}

output "rds_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.database.endpoint
}