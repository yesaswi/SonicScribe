output "bucket_name" {
  value       = module.storage.bucket_name
  description = "The name of the Cloud Storage bucket"
}

output "function_name" {
  value       = module.functions.function_name
  description = "The name of the deployed Cloud Function"
}

output "function_url" {
  value       = module.functions.function_url
  description = "The URL of the deployed Cloud Function"
}