

resource "observe_dataset" "process_info" {
    acceleration_disabled = false
    freshness             = "2m0s"
    inputs                = {
        "Custom SIEM/Process Monitoring" = "o:::dataset:47769901"
    }
    name                  = "Custom SIEM/Process Info"
    workspace             = "o:::workspace:43784541"

    stage {
        output_stage = false
        pipeline     = <<-EOT
            make_col command_line:string(FIELDS.command_line),
                host:string(FIELDS.host),
                process_name:string(FIELDS.process_name)
            make_col user:string(FIELDS.user)
        EOT
    }
}

