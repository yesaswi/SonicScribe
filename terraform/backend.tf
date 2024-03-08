terraform {
  backend "gcs" {
    bucket = "sonicscribe-terraform-state"
    prefix = "terraform/state"
  }
}