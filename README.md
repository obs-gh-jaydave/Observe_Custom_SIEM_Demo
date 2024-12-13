# Observe SIEM Demo

This repository contains a demonstration environment for showcasing how [Observe](https://www.observeinc.com/) can ingest, correlate, and alert on SIEM-like data. It simulates both normal and malicious activity within a fictional mid-sized enterprise network, allowing you to visualize common security scenarios, such as successful/failed logins, brute force attempts, malicious DNS queries, lateral movement, and suspicious process execution.

## Overview

The demo environment includes:
- A Docker container and Python script (`generate_events.py`) to continuously send mock SIEM data (authentication, DNS queries, and process creation logs) to Observe.
- Sample Terraform configurations for creating Observe dashboards and datasets.
- A storyline that transitions from normal baseline activity to increasingly suspicious and malicious behavior, illustrating how Observe can detect, alert, and visualize these patterns.

## Files and Directories

- **Dockerfile**: Builds the container image that runs `generate_events.py`.
- **docker-compose.yml**: Simplifies running the container locally.
- **src/generate_events.py**: Python script that generates both normal and malicious events and sends them to the Observe HTTP endpoint.
- **src/requirements.txt**: Python dependencies for the event generation script.
- **README.md**: This documentation file, describing the environment and how to use it.

## Scenario Context and Storyline

This demo represents a common SIEM scenario:

1. **Initial Baseline (Normal Activity)**  
   - Steady, successful user logins from known internal or well-known public IP ranges.  
   - Normal DNS queries to internal domains like `intranet.local`.  
   - Routine process executions (e.g., `chrome.exe`, `excel.exe`) on various hosts.

2. **First Signs of Suspicious Activity (Brute Forcing)**  
   - A spike in failed login attempts targeting the `jdoe` account from a foreign IP (e.g., `203.0.113.42`).  
   - Eventually, a successful login from this suspicious IP, indicating a potential credential compromise.

3. **Lateral Movement & Suspicious Tools**  
   - The compromised user (`jdoe`) begins logging into multiple internal servers in quick succession (lateral movement).  
   - Endpoint logs show suspicious process creation events, such as a `powershell.exe` command downloading `mim.ps1` from `malicious.example.com`.

4. **Malicious DNS Queries & Potential Exfiltration**  
   - DNS queries to known malicious domains appear, suggesting command-and-control activity.  
   - Potential outbound data transfers (large traffic volumes) indicate possible data exfiltration attempts.

5. **Observe Dashboards & Alerts**  
   Within Observe, you can build dashboards and alerts to:
   - Show KPIs for successful vs. failed logins.
   - Highlight time-series charts of authentication events and DNS queries.
   - Surface alerts when brute force detections trigger, suspicious processes are run, or malicious domains are contacted.
   - Drill down into individual events and correlate user, host, and IP information to understand the attack narrative.

## Running the Demo

1. **Set Environment Variables for Observe**  
   Set `OBSERVE_ENDPOINT` and `AUTH_TOKEN` as environment variables in `docker-compose.yml` or directly at runtime:
   ```bash
   export OBSERVE_ENDPOINT="https://<your_observe_customer>.collect.observeinc.com/v1/http"
   export AUTH_TOKEN="your_datastream_token"
   
2.  **Build and Run**

    ```bash
    docker-compose up -d
    ```
## View in Observe

Navigate to your Observe workspace and view the configured datasets and dashboards.

- You can import the provided Terraform config (below) to set up a custom dashboard.
- Explore the data using queries and build visuals to see normal vs. malicious patterns evolve over time.

## Terraform Configuration for Dashboards and Datasets

The provided Terraform resources illustrate how to define Observe datasets and a dashboard to visualize the SIEM data.

### Dashboards

**Custom SIEM/User Overview Dashboard:**

The included Terraform configuration sets up a dashboard with parameters for filtering by `User` or `threat_indicator`. It includes:

- Single-value panels for successful and failed logins.
- Charts for brute force activity and suspicious process events over time.
- Panels for malicious DNS queries and lateral movement.
- A text card explaining the “Superman problem” in SIEM.

### Datasets

**Example Datasets:**

- **DNS Query Dataset:** Filters raw SIEM logs for `event_type = "dns_query"` to identify normal and malicious DNS lookups.
- **Failed Logins Dataset:** Filters logs for `status = "failed"` to spotlight brute force activity.
- **Process Info Dataset:** Extracts process creation events to monitor for suspicious commands or lateral movement.
- **Process Monitoring Dataset:** Filters out only `process_create` events for deeper analysis.
- **Raw SIEM Logs Dataset:** The foundational dataset ingesting all events from the Observe HTTP endpoint.

By applying the Terraform configurations, you can quickly stand up a curated environment where your raw SIEM logs feed into specialized datasets and are visualized on a user-friendly dashboard.

## The “Superman Problem”

As highlighted in the Terraform snippet’s text card, the “Superman problem” refers to the unrealistic expectation that a single SIEM solution can handle every security challenge flawlessly. Instead, a SIEM should be part of a broader security strategy that involves careful tuning, skilled analysts, and integration with other tools.
