module "storage" {
  source              = "./modules/storage"
  audio_bucket_name   = "sonicscribe-audio-bucket"
  function_bucket_name = "sonicscribe-function-bucket"
  region              = var.region
}

module "cloud_function_iam" {
  source                = "./modules/iam"
  project_id            = var.project_id
  function_name         = module.functions.function_name
  bucket_name           = module.storage.audio_bucket_name
  service_account_email = google_service_account.cloud_function_service_account.email
}

resource "google_service_account" "cloud_function_service_account" {
  account_id   = "cloud-function-service-account"
  display_name = "Cloud Function Service Account"
}

module "functions" {
  source                = "./modules/functions"
  function_name         = "upload_audio"
  function_entry_point  = "upload_audio"
  function_source_dir   = "../functions/upload_audio"
  function_output_path  = "../upload_audio.zip"
  function_runtime      = "python310"
  function_bucket_name  = module.storage.function_bucket_name
  service_account_email = google_service_account.cloud_function_service_account.email
  region                = var.region
}
