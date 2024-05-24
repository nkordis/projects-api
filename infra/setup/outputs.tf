output "cd_user_access_key_id" {
  description = "The access key ID for CD user"
  value       = aws_iam_access_key.cd.id
}

output "cd_user_access_key_secret" {
  description = "The secret access key for CD user"
  value       = aws_iam_access_key.cd.secret
  sensitive   = true
}
