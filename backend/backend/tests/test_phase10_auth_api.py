from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pytest

from app.core.dependencies import get_current_active_user
from app.main import app
from app.models.user import User
from app.schemas.auth import AuthSessionData, LogoutData, TokenPair
from app.schemas.user import UserRead
from app.services.auth_service import AuthService


@pytest.fixture
def auth_user_read() -> UserRead:
    now = datetime(2026, 6, 22, 0, 0, 0)
    return UserRead(
        id=uuid4(),
        username="captain_one",
        email="captain@example.com",
        avatar_url=None,
        bio=None,
        xp=25,
        level=1,
        rank_title="Cadet",
        streak_days=1,
        last_login_date=None,
        status="ACTIVE",
        role="USER",
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def auth_session_data(auth_user_read: UserRead) -> AuthSessionData:
    return AuthSessionData(
        user=auth_user_read,
        tokens=TokenPair(
            access_token="access-token",
            refresh_token="refresh-token",
            token_type="bearer",
            expires_in=86400,
        ),
    )


def test_auth_register_login_refresh_routes(client, monkeypatch, auth_session_data: AuthSessionData):
    async def fake_register(*args, **kwargs):
        return auth_session_data

    async def fake_login(*args, **kwargs):
        return auth_session_data

    async def fake_refresh(*args, **kwargs):
        return auth_session_data

    monkeypatch.setattr(AuthService, "register", fake_register)
    monkeypatch.setattr(AuthService, "login", fake_login)
    monkeypatch.setattr(AuthService, "refresh", fake_refresh)

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "captain_one",
            "email": "captain@example.com",
            "password": "StrongPass1",
            "confirm_password": "StrongPass1",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "captain@example.com", "password": "StrongPass1"},
    )
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "refresh-token-value-1234567890"},
    )

    assert register_response.status_code == 201
    assert login_response.status_code == 200
    assert refresh_response.status_code == 200
    assert register_response.json()["data"]["user"]["username"] == "captain_one"
    assert login_response.json()["data"]["tokens"]["access_token"] == "access-token"


def test_auth_me_and_logout_routes(client, monkeypatch, auth_user_read: UserRead):
    current_user = User(
        id=auth_user_read.id,
        username=auth_user_read.username,
        email=auth_user_read.email,
        password_hash="hashed",
        xp=auth_user_read.xp,
        level=auth_user_read.level,
        rank_title=auth_user_read.rank_title,
        streak_days=auth_user_read.streak_days,
        status=auth_user_read.status,
        role=auth_user_read.role,
    )

    async def fake_current_user() -> User:
        return current_user

    async def fake_get_current_user_data(*args, **kwargs):
        return auth_user_read

    async def fake_logout(*args, **kwargs):
        return LogoutData(logged_out=True)

    app.dependency_overrides[get_current_active_user] = fake_current_user
    monkeypatch.setattr(AuthService, "get_current_user_data", fake_get_current_user_data)
    monkeypatch.setattr(AuthService, "logout", fake_logout)

    try:
        me_response = client.get("/api/v1/auth/me")
        logout_response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "refresh-token-value-1234567890"},
        )
    finally:
        app.dependency_overrides.clear()

    assert me_response.status_code == 200
    assert logout_response.status_code == 200
    assert me_response.json()["data"]["user"]["email"] == "captain@example.com"
    assert logout_response.json()["data"]["logged_out"] is True
