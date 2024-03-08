resource "google_storage_bucket" "audio_bucket" {
  name          = var.audio_bucket_name
  location      = var.region
  force_destroy = true
  
  uniform_bucket_level_access = true

  public_access_prevention = "enforced"
  
  versioning {
    enabled = false
  }

  storage_class = "STANDARD"
}

resource "google_storage_bucket" "function_bucket" {
  name          = var.function_bucket_name
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  public_access_prevention = "enforced"
  
  versioning {
    enabled = true
  }

  storage_class = "STANDARD"
}