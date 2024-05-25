variable "tf_state_bucket" {
  description = "Name of S3 bucket in AWS for storing TF state"
  default     = "projects-api-terraform-state"
}

variable "tf_state_lock_table" {
  description = "Name of DynamoDB table in AWS for locking TF state"
  default     = "projects-api-terraform-lock"
}

variable "project" {
  description = "Name of project"
  default     = "projects-api"
}

variable "contact" {
  description = "Contact email address"
  default     = "nikoskordis@gmail.com"
}
