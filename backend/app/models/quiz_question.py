from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import JSONDictList, QuestionType, build_sa_enum


class QuizQuestion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a quiz question belonging to a planet."""

    __tablename__ = "quiz_questions"
    __table_args__ = (
        UniqueConstraint("planet_id", "order_number", name="uq_quiz_questions_planet_order_number"),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="quiz_questions_difficulty_range"),
        CheckConstraint("xp_reward >= 0", name="quiz_questions_xp_reward_non_negative"),
    )

    planet_id: Mapped[UUID] = mapped_column(ForeignKey("planets.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(
        build_sa_enum(QuestionType, name="question_type_enum", length=50),
        nullable=False,
        index=True,
    )
    options: Mapped[JSONDictList | None] = mapped_column(JSONB, nullable=True)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)

    planet: Mapped["Planet"] = relationship(back_populates="quiz_questions")
