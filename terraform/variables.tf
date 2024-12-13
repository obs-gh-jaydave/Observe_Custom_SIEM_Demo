variable "observe_customer_id" {
  type        = string
  description = "The customer ID for your Observe account (e.g., 123456789012)."
}

variable "observe_api_token" {
  type        = string
  description = "The API token for your Observe account."
  sensitive   = true
}

variable "workspace_id" {
  type        = string
  description = "The workspace ID to use for Observe resources."
  # If you have a known workspace ID, you can set a default here or supply it via tfvars.
  # default = "o:::workspace:43784541"
}