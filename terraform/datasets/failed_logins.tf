

resource "observe_dataset" "failed_logins" {
    acceleration_disabled = false
    freshness             = "2m0s"
    inputs                = {
        "Custom SIEM/User Logins From Internal IP Ranges" = "o:::dataset:47769860"
    }
    name                  = "Custom SIEM/Failed Logins"
    workspace             = "o:::workspace:43784541"

    stage {
        output_stage = false
        pipeline     = <<-EOT
            make_col status:string(FIELDS.status)
            filter status = "failed"
        EOT
    }
}

