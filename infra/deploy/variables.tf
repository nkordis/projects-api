variable "prefix" {
  description = "Prefix for resources"
  default     = "pa"
}

variable "project" {
  description = "Name of project"
  default     = "projects-api"
}

variable "contact" {
  description = "Contact email address"
  default     = "nikoskordis@gmail.com"
}

variable "db_username" {
  description = "Username for the projects api app database"
  default     = "projectsapi"
}

variable "db_password" {
  description = "Password for the projects api app database"
  default     = "projectsapi"
}
