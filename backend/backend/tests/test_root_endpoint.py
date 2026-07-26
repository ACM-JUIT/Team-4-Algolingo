from __future__ import annotations


def test_root_endpoint_returns_public_metadata(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "AlgoLingo API"
    assert payload["status"] == "running"
    assert payload["health"] == "/health"
