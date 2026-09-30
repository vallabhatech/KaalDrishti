import os

os.environ["KAALDRISHTI_API_TOKEN"] = "test-token"

from server import app


def event(event_type="auth.bruteforce"):
    return {
        "event_id": "test-1",
        "client": "pytest",
        "event_type": event_type,
        "message": "synthetic test",
        "source": "simulator",
        "metadata": {"lab": True, "authorized": True},
    }


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200


def test_auth_required():
    response = app.test_client().post("/api/events", json=event())
    assert response.status_code == 401


def test_unauthorized_source_rejected():
    payload = event()
    payload["source"] = "device"
    response = app.test_client().post("/api/events", headers={"X-API-Key": "test-token"}, json=payload)
    assert response.status_code == 400


def test_unknown_event_rejected():
    response = app.test_client().post(
        "/api/events", headers={"X-API-Key": "test-token"}, json=event("unknown")
    )
    assert response.status_code == 422


def test_event_detected_and_accepted():
    response = app.test_client().post(
        "/api/events", headers={"X-API-Key": "test-token"}, json=event()
    )
    assert response.status_code == 202
    assert response.json["detection"]["severity"] == "high"
    assert response.json["detection"]["technique"] == "T1110"
