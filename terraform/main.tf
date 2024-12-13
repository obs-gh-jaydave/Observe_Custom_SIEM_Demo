terraform {
  required_version = ">= 0.13"
  required_providers {
    observe = {
      source  = "observeinc/observe"
      version = "~> 1.0"
    }
  }
}

provider "observe" {
  # Authentication configuration here.
}
