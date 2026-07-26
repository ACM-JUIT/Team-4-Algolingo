from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import JSONDictList


class QuizAttempt(UUIDPrimaryKeyMixin, Base):
    """Represents a user's submitted quiz attempt."""

    __tablename__ = "quiz_attempts"
    __table_args__ = (
        CheckConstraint("score >= 0", name="quiz_attempts_score_non_negative"),
        CheckConstraint("total_questions >= 0", name="quiz_attempts_total_questions_non_negative"),
        CheckConstraint("xp_earned >= 0", name="quiz_attempts_xp_earned_non_negative"),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    planet_id: Mapped[UUID] = mapped_column(ForeignKey("planets.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    answers: Mapped[JSONDictList | None] = mapped_column(JSONB, nullable=True)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    user: Mapped["User"] = relationship(back_populates="quiz_attempts")
    planet: Mapped["Planet"] = relationship(back_populates="quiz_attempts")
