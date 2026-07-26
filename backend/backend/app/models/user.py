from __future__ import annotations

from datetime import date

from sqlalchemy import CheckConstraint, Date, Index, Integer, String, desc, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import RankTitle, UserRole, UserStatus, build_sa_enum


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a learner account within AlgoLingo."""

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("xp >= 0", name="users_xp_non_negative"),
        CheckConstraint("level >= 1", name="users_level_minimum"),
        CheckConstraint("char_length(username) >= 3", name="users_username_min_length"),
        CheckConstraint("char_length(email) >= 5", name="users_email_min_length"),
        Index("ix_users_xp_desc", desc("xp")),
    )

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    rank_title: Mapped[RankTitle] = mapped_column(
        build_sa_enum(RankTitle, name="rank_title_enum", length=50),
        nullable=False,
        default=RankTitle.CADET,
        server_default=text("'Cadet'"),
    )
    streak_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    last_login_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[UserStatus] = mapped_column(
        build_sa_enum(UserStatus, name="user_status_enum", length=20),
        nullable=False,
        default=UserStatus.ACTIVE,
        server_default=text("'ACTIVE'"),
        index=True,
    )
    role: Mapped[UserRole] = mapped_column(
        build_sa_enum(UserRole, name="user_role_enum", length=20),
        nullable=False,
        default=UserRole.USER,
        server_default=text("'USER'"),
        index=True,
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    user_progress_entries: Mapped[list["UserProgress"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    user_artifacts: Mapped[list["UserArtifact"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    daily_logins: Mapped[list["DailyLogin"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    leaderboard_snapshots: Mapped[list["LeaderboardSnapshot"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    nova_sessions: Mapped[list["NovaSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    user_events: Mapped[list["UserEvent"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
