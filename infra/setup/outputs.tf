output "cd_user_access_key_id" {
  description = "The access key ID for CD user"
  value       = aws_iam_access_key.cd.id
}

output "cd_user_access_key_secret" {
  description = "The secret access key for CD user"
  value       = aws_iam_access_key.cd.secret
  sensitive   = true
}

output "ecr_repo_app" {
  description = "ECR repository URL for app image"
  value       = aws_ecr_repository.app.repository_url
}

output "ecr_repo_proxy" {
  description = "ECR repository URL for proxy image"
  value       = aws_ecr_repository.proxy.repository_url
}
