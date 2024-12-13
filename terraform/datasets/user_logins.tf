

resource "observe_dataset" "user_logins_from_internal_ip_ranges" {
    acceleration_disabled = false
    freshness             = "2m0s"
    inputs                = {
        "Custom SIEM/Raw SIEM Logs" = "o:::dataset:47769846"
    }
    name                  = "Custom SIEM/User Logins From Internal IP Ranges"
    workspace             = "o:::workspace:43784541"

    stage {
        output_stage = false
        pipeline     = <<-EOT
            make_col event_type:string(FIELDS.event_type)
            filter event_type = "authentication"
        EOT
    }
}

