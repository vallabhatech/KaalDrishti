"""KaalDrishti authenticated defensive telemetry API."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, jsonify, request

from config import API_TOKEN, MAX_REQUEST_BYTES, PORT
from detection import detect
from storage import EventStore

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES
store = EventStore()


def authorized() -> bool:
    return bool(API_TOKEN) and request.headers.get("X-API-Key") == API_TOKEN


@app.get("/")
def home():
    return jsonify(service="KaalDrishti", purpose="endpoint threat detection lab", status="ok")


@app.get("/health")
def health():
    return jsonify(status="ok", authentication_configured=bool(API_TOKEN))


@app.get("/api/events")
def recent_events():
    if not authorized():
        return jsonify(error="unauthorized"), 401
    return jsonify(events=store.recent())


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

    if payload["source"] != "simulator" or payload.get("metadata", {}).get("authorized") is not True:
        return jsonify(error="only authorized simulated lab events are accepted"), 400

    detection = detect(payload)
    if detection is None:
        return jsonify(error="unsupported event type"), 422

    received_at = datetime.now(timezone.utc).isoformat()
    store.save(payload, detection.__dict__, received_at)
    return jsonify(
        status="accepted",
        event_id=payload["event_id"],
        detection=detection.__dict__,
        received_at=received_at,
    ), 202


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="request too large"), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
