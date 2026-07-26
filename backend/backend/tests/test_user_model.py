from __future__ import annotations

from app.models.refresh_token import RefreshToken
from app.models.user import User


def test_user_model_contains_auth_columns() -> None:
    columns = User.__table__.columns.keys()

    assert "username" in columns
    assert "email" in columns
    assert "password_hash" in columns
    assert "status" in columns
    assert "role" in columns


def test_refresh_token_model_contains_rotation_columns() -> None:
    columns = RefreshToken.__table__.columns.keys()

    assert "user_id" in columns
    assert "token_hash" in columns
    assert "expires_at" in columns
    assert "revoked" in columns
