resource "google_cloud_run_service_iam_binding" "binding" {
  service  = var.function_name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}

resource "google_storage_bucket_iam_member" "storage_object_creator" {
  bucket = var.bucket_name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${var.service_account_email}"
}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = var.project_id
  cloud_function = var.function_name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}

resource "google_project_iam_member" "cloud_function_service_account_roles" {
  for_each = toset([
    "roles/cloudfunctions.developer",
    "roles/storage.objectAdmin",
    # Add other required roles
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${var.service_account_email}"
}