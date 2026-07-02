from __future__ import annotations


def test_health_check(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "AlgoLingo Backend"


def test_api_health_check(client) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["environment"] in {"development", "testing", "staging", "production"}
