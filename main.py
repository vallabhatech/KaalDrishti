"""KaalDrishti client: consent-based security telemetry simulator."""

from __future__ import annotations

import os
import time
import uuid

import requests

from config import CLOUD_ENDPOINT, API_TOKEN, CLIENT_NAME, SEND_INTERVAL_SECONDS


def build_event(event_type: str, message: str) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "client": CLIENT_NAME,
        "event_type": event_type,
        "message": message,
        "source": "synthetic",
    }


def send_event(event: dict) -> bool:
    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["X-API-Key"] = API_TOKEN
    try:
        response = requests.post(
            CLOUD_ENDPOINT,
            json=event,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        print(f"✓ event accepted: {event['event_id']}")
        return True
    except requests.RequestException as exc:
        print(f"✗ event delivery failed: {exc}")
        return False


def main() -> None:
    print("KaalDrishti — consent-based telemetry lab")
    print("No keyboard, clipboard, camera, screenshot, or persistence collection is performed.")
    print(f"Sending synthetic security events every {SEND_INTERVAL_SECONDS}s. Press Ctrl+C to stop.\n")

    sequence = 0
    while True:
        sequence += 1
        event = build_event(
            "demo.security_event",
            f"Synthetic security event #{sequence} generated for lab testing.",
        )
        send_event(event)
        time.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped cleanly.")
