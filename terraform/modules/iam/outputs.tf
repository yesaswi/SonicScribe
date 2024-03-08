output "function_invoker_role" {
  value       = google_cloudfunctions_function_iam_member.invoker.role
  description = "The IAM role for invoking the Cloud Function"
}

output "storage_object_creator_role" {
  value       = google_storage_bucket_iam_member.storage_object_creator.role
  description = "The IAM role for creating objects in the Cloud Storage bucket"
}