from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import JSONStringList, ProgressStatus, build_sa_enum


class UserProgress(UUIDPrimaryKeyMixin, Base):
    """Represents a user's persistent progress on a planet."""

    __tablename__ = "user_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "planet_id", name="uq_user_progress_user_planet"),
        CheckConstraint("xp_earned >= 0", name="user_progress_xp_earned_non_negative"),
        CheckConstraint(
            "quiz_best_score IS NULL OR quiz_best_score >= 0",
            name="user_progress_quiz_best_score_non_negative",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    planet_id: Mapped[UUID] = mapped_column(ForeignKey("planets.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_discoveries: Mapped[JSONStringList] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    completed_practices: Mapped[JSONStringList] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    quiz_passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))
    quiz_best_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))
    status: Mapped[ProgressStatus] = mapped_column(
        build_sa_enum(ProgressStatus, name="progress_status_enum", length=20),
        nullable=False,
        default=ProgressStatus.NOT_STARTED,
        server_default=text("'NOT_STARTED'"),
        index=True,
    )
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="user_progress_entries")
    planet: Mapped["Planet"] = relationship(back_populates="user_progress_entries")
