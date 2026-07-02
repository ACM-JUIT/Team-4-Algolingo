from __future__ import annotations

from datetime import date

from app.services.auth_service import AuthService


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
