from __future__ import annotations

from app.db.base import Base
from app.models import (  # noqa: F401
    Artifact,
    DailyLogin,
    Discovery,
    Galaxy,
    LeaderboardSnapshot,
    NovaMessage,
    NovaSession,
    Planet,
    PracticeChallenge,
    QuizAttempt,
    QuizQuestion,
    RefreshToken,
    User,
    UserArtifact,
    UserEvent,
    UserProgress,
)
from app.models.planet import Planet
from app.models.user_progress import UserProgress


EXPECTED_TABLES = {
    "artifacts",
    "daily_logins",
    "discoveries",
    "galaxies",
    "leaderboard_snapshots",
    "nova_messages",
    "nova_sessions",
    "planets",
    "practice_challenges",
    "quiz_attempts",
    "quiz_questions",
    "refresh_tokens",
    "user_artifacts",
    "user_events",
    "user_progress",
    "users",
}


def test_all_required_tables_are_registered() -> None:
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables.keys()))


def test_planet_has_expected_foreign_keys() -> None:
    foreign_key_targets = {fk.target_fullname for fk in Planet.__table__.foreign_keys}

    assert "galaxies.id" in foreign_key_targets
    assert "artifacts.id" in foreign_key_targets


def test_user_progress_has_unique_user_planet_constraint() -> None:
    constraint_names = {constraint.name for constraint in UserProgress.__table__.constraints}

    assert "uq_user_progress_user_planet" in constraint_names
