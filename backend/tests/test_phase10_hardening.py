from __future__ import annotations

from uuid import uuid4

from app.core.dependencies import get_current_active_user
from app.main import app
from app.models.user import User
from app.services.dashboard_service import DashboardService


def test_security_headers_and_request_headers_present(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time-MS" in response.headers


def test_protected_route_returns_consistent_unauthorized_error(client) -> None:
    response = client.get("/api/v1/dashboard")

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "Not authenticated"


def test_validation_error_returns_consistent_format(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "ab",
            "email": "not-an-email",
            "password": "weak",
            "confirm_password": "weak",
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "Validation failed"
    assert "errors" in payload


def test_generic_exception_handler_returns_internal_server_error(client, monkeypatch) -> None:
    async def fake_current_user() -> User:
        return User(
            id=uuid4(),
            username="captain_one",
            email="captain@example.com",
            password_hash="hashed",
            xp=0,
            level=1,
            rank_title="Cadet",
            streak_days=0,
            status="ACTIVE",
            role="USER",
        )

    async def broken_dashboard(*args, **kwargs):
        raise RuntimeError("boom")

    app.dependency_overrides[get_current_active_user] = fake_current_user
    monkeypatch.setattr(DashboardService, "get_dashboard", broken_dashboard)
    original_debug = app.debug
    app.debug = False
    try:
        response = client.get("/api/v1/dashboard")
    finally:
        app.debug = original_debug
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.text
