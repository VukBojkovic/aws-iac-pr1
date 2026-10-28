resource "aws_ecr_repository" "app_repo" {
  name                 = "aws-iac-pr1-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "aws-iac-pr1-ecr"
  }
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.app_repo.repository_url
  description = "URL of the ECR repository for Docker images"
}