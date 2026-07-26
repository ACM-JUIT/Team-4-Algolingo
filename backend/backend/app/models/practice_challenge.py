from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ChallengeType, JSONDictList, JSONStringList, PracticeStatus, build_sa_enum


class PracticeChallenge(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a hands-on practice challenge for a planet."""

    __tablename__ = "practice_challenges"
    __table_args__ = (
        UniqueConstraint("planet_id", "order_number", name="uq_practice_challenges_planet_order_number"),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="practice_challenges_difficulty_range"),
        CheckConstraint("xp_reward >= 0", name="practice_challenges_xp_reward_non_negative"),
        CheckConstraint("char_length(title) >= 1", name="practice_challenges_title_min_length"),
    )

    planet_id: Mapped[UUID] = mapped_column(ForeignKey("planets.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    challenge_type: Mapped[ChallengeType] = mapped_column(
        build_sa_enum(ChallengeType, name="challenge_type_enum", length=50),
        nullable=False,
        index=True,
    )
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    solution_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    hints: Mapped[JSONStringList] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    test_cases: Mapped[JSONDictList] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[PracticeStatus] = mapped_column(
        build_sa_enum(PracticeStatus, name="practice_status_enum", length=20),
        nullable=False,
        default=PracticeStatus.LOCKED,
        server_default=text("'LOCKED'"),
        index=True,
    )

    planet: Mapped["Planet"] = relationship(back_populates="practice_challenges")
