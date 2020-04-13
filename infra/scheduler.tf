resource "google_cloud_scheduler_job" "generate_climate_news" {
  name        = "generate-climate-news"
  region      = var.region
  description = "generate daily climate news"
  schedule    = "0 9 * * *"
  time_zone   = "Europe/London"

  http_target {
    http_method = "POST"
    uri         = "https://cloudbuild.googleapis.com/v1/projects/${var.orchestration_project}/triggers/BUILD-generate-climate-news:run"
    body        = base64encode("{\"branchName\":\"master\"}")

    oauth_token {
      service_account_email = "${var.orchestration_project}@appspot.gserviceaccount.com"
    }
  }
}
