import os

os.environ["KAALDRISHTI_API_TOKEN"] = "test-token"

from server import app


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_event_requires_authentication():
    response = app.test_client().post("/api/events", json={})
    assert response.status_code == 401


def test_event_rejects_non_synthetic_source():
    client = app.test_client()
    response = client.post(
        "/api/events",
        headers={"X-API-Key": "test-token"},
        json={
            "event_id": "1",
            "client": "test",
            "event_type": "demo",
            "message": "hello",
            "source": "device",
        },
    )
    assert response.status_code == 400


def test_event_is_accepted():
    client = app.test_client()
    response = client.post(
        "/api/events",
        headers={"X-API-Key": "test-token"},
        json={
            "event_id": "1",
            "client": "test",
            "event_type": "demo",
            "message": "hello",
            "source": "synthetic",
        },
    )
    assert response.status_code == 202
    assert response.json["status"] == "accepted"
