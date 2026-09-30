"""Flask receiver for consent-based KaalDrishti telemetry events."""

from __future__ import annotations

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_REQUEST_BYTES", "65536"))
API_TOKEN = os.getenv("KAALDRISHTI_API_TOKEN", "")


def authorized() -> bool:
    return bool(API_TOKEN) and request.headers.get("X-API-Key") == API_TOKEN


@app.get("/")
def home():
    return jsonify(service="KaalDrishti Telemetry API", status="ok")


@app.get("/health")
def health():
    return jsonify(status="ok", authentication_configured=bool(API_TOKEN))


@app.post("/api/events")
def ingest_event():
    if not authorized():
        return jsonify(error="unauthorized"), 401

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="request body must be a JSON object"), 400

    required = ("event_id", "client", "event_type", "message", "source")
    missing = [key for key in required if not payload.get(key)]
    if missing:
        return jsonify(error="missing required fields", fields=missing), 400

    if payload["source"] != "synthetic":
        return jsonify(error="only synthetic lab events are accepted"), 400

    record = {
        **{key: payload[key] for key in required},
        "received_at": datetime.now(timezone.utc).isoformat(),
    }
    print(f"event={record['event_id']} type={record['event_type']} client={record['client']}")
    return jsonify(status="accepted", event=record), 202


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="request too large"), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
