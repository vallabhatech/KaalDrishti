"""KaalDrishti defensive telemetry simulator and API client."""

from __future__ import annotations

import time
import uuid

import requests

from config import API_TOKEN, CLOUD_ENDPOINT, CLIENT_NAME, SEND_INTERVAL_SECONDS


SCENARIOS = [
    ("auth.bruteforce", "Multiple failed authentication attempts detected."),
    ("process.suspicious", "A simulated process matches a suspicious execution rule."),
    ("persistence.attempt", "A simulated persistence modification was observed."),
    ("network.anomaly", "A simulated endpoint made an unexpected outbound connection."),
    ("file.integrity", "A simulated protected-file integrity change was detected."),
]


def build_event(event_type: str, message: str) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "client": CLIENT_NAME,
        "event_type": event_type,
        "message": message,
        "source": "simulator",
        "severity": "medium",
        "metadata": {"lab": True, "authorized": True},
    }


def send_event(event: dict) -> bool:
    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["X-API-Key"] = API_TOKEN
    try:
        response = requests.post(CLOUD_ENDPOINT, json=event, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"accepted {event['event_type']} -> {event['event_id']}")
        return True
    except requests.RequestException as exc:
        print(f"delivery failed: {exc}")
        return False


def main() -> None:
    print("KaalDrishti — endpoint threat detection lab")
    print("Synthetic defensive scenarios only; no user-content or sensor capture is performed.")
    sequence = 0
    while True:
        event_type, message = SCENARIOS[sequence % len(SCENARIOS)]
        sequence += 1
        send_event(build_event(event_type, message))
        time.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped cleanly.")
