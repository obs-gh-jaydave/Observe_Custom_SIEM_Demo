

resource "observe_dataset" "raw_siem_logs" {
    acceleration_disabled = false
    freshness             = "2m0s"
    inputs                = {
        "SIEM-Demo_47769845" = "o:::dataset:47769845"
    }
    name                  = "Custom SIEM/Raw SIEM Logs"
    workspace             = "o:::workspace:43784541"

    stage {
        output_stage = false
        pipeline     = "filter DATASTREAM_TOKEN_ID = \"ds1oHg1vndZWLugI5UOa\""
    }
}

