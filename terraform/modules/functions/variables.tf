variable "function_name" {
  description = "The name of the Cloud Function"
}

variable "function_entry_point" {
  description = "The name of the function that will be executed"
}

variable "function_source_dir" {
  description = "The directory containing the function source code"
}

variable "function_output_path" {
  description = "The output path for the function source archive"
}

variable "function_runtime" {
  description = "The runtime environment for the Cloud Function"
}

variable "function_bucket_name" {
  description = "The name of the Cloud Storage bucket for function source code"
}

variable "audio_bucket_name" {
  description = "The name of the Cloud Storage bucket for audio files"
}

variable "service_account_email" {
  description = "The email of the service account used by the Cloud Function"
}

variable "region" {
  description = "The region in which the Cloud Function will be deployed"
}

variable "project_id" {
  description = "The GCP project ID"
}

variable "function_archive_name" {
  description = "The name of the Cloud Function source archive"
}
