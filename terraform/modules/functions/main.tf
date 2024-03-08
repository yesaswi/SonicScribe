data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = var.function_source_dir
  output_path = var.function_output_path
}

resource "google_storage_bucket_object" "function_archive" {
  name   = var.function_archive_name
  bucket = var.function_bucket_name
  source = data.archive_file.function_source.output_path
}

resource "google_cloudfunctions2_function" "function" {
  name        = var.function_name
  description = "Cloud Function to upload audio files"
  location    = var.region

  build_config {
    runtime     = var.function_runtime
    entry_point = var.function_entry_point
    source {
      storage_source {
        bucket = var.function_bucket_name
        object = google_storage_bucket_object.function_archive.name
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60
    service_account_email = var.service_account_email
    environment_variables = {
        AUDIO_BUCKET_NAME = var.audio_bucket_name
    }
  }
}
