output "raw_siem_logs_id" {
  description = "The ID of the Custom SIEM/Raw SIEM Logs dataset."
  value       = observe_dataset.raw_siem_logs.id
}

output "user_overview_dashboard_url" {
  description = "The URL of the Custom SIEM/User Overview Dashboard."
  # Assuming the provider returns a URL attribute for dashboards:
  # Check the provider docs for what attributes are exposed by the dashboard resource.
  value = observe_dashboard.user_overview_dashboard.url
}