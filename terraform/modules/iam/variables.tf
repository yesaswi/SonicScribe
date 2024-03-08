variable "project_id" {
  description = "The ID of the GCP project"
}

variable "function_name" {
  description = "The name of the Cloud Function"
}

variable "bucket_name" {
  description = "The name of the Cloud Storage bucket"
}

variable "service_account_email" {
  description = "The email address of the service account used by the Cloud Function"
}