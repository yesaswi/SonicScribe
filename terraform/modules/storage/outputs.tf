output "audio_bucket_name" {
  value       = google_storage_bucket.audio_bucket.name
  description = "The name of the Cloud Storage bucket for audio files"
}

output "function_bucket_name" {
  value       = google_storage_bucket.function_bucket.name
  description = "The name of the Cloud Storage bucket for function source code"
}