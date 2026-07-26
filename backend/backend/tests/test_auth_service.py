from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

import pytest

from app.models.user import User
from app.services.auth_service import AuthService


class FakeSession:
    def __init__(self) -> None:
        self.refresh_calls = 0
        self.added = []
        self.flushed = False

    def add(self, instance) -> None:
        self.added.append(instance)

    async def flush(self) -> None:
        self.flushed = True

    async def refresh(self, user: User) -> None:
        self.refresh_calls += 1
        now = datetime(2026, 1, 1, 12, 0, 0)
        user.created_at = now
        user.updated_at = now


def test_calculate_streak_for_first_login() -> None:
    result = AuthService.calculate_streak(last_login_date=None, current_streak=0, today=date(2026, 6, 22))

    assert result.streak_days == 1
    assert result.first_login_today is True


def test_calculate_streak_for_same_day_login() -> None:
    result = AuthService.calculate_streak(last_login_date=date(2026, 6, 22), current_streak=5, today=date(2026, 6, 22))

    assert result.streak_days == 5
    assert result.first_login_today is False


def test_calculate_streak_for_consecutive_day_login() -> None:
    result = AuthService.calculate_streak(last_login_date=date(2026, 6, 21), current_streak=5, today=date(2026, 6, 22))

    assert result.streak_days == 6
    assert result.first_login_today is True


def test_calculate_streak_for_broken_streak() -> None:
    result = AuthService.calculate_streak(last_login_date=date(2026, 6, 18), current_streak=5, today=date(2026, 6, 22))

    assert result.streak_days == 1
    assert result.first_login_today is True


@pytest.mark.asyncio
async def test_issue_tokens_refreshes_user_before_serialization() -> None:
    session = FakeSession()
    user = User(
        id=uuid4(),
        username="captain_one",
        email="captain@example.com",
        password_hash="hashed",
        xp=0,
        level=1,
        rank_title="Cadet",
        streak_days=1,
        status="ACTIVE",
        role="USER",
    )

    auth_session = await AuthService._issue_tokens(session=session, user=user)

    assert session.flushed is True
    assert session.refresh_calls == 1
    assert auth_session.user.username == "captain_one"
    assert auth_session.tokens.access_token
    assert auth_session.tokens.refresh_token
