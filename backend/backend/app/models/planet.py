from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PlanetStatus, build_sa_enum


class Planet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a programming planet inside a galaxy."""

    __tablename__ = "planets"
    __table_args__ = (
        UniqueConstraint("galaxy_id", "order_number", name="uq_planets_galaxy_order_number"),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="planets_difficulty_range"),
        CheckConstraint("xp_total >= 0", name="planets_xp_total_non_negative"),
        CheckConstraint(
            "estimated_time_minutes IS NULL OR estimated_time_minutes >= 0",
            name="planets_estimated_time_non_negative",
        ),
        CheckConstraint("char_length(name) >= 1", name="planets_name_min_length"),
    )

    galaxy_id: Mapped[UUID] = mapped_column(ForeignKey("galaxies.id", ondelete="CASCADE"), nullable=False, index=True)
    artifact_id: Mapped[UUID | None] = mapped_column(ForeignKey("artifacts.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tagline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    xp_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    estimated_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[PlanetStatus] = mapped_column(
        build_sa_enum(PlanetStatus, name="planet_status_enum", length=20),
        nullable=False,
        default=PlanetStatus.LOCKED,
        server_default=text("'LOCKED'"),
        index=True,
    )
    unlock_condition: Mapped[str | None] = mapped_column(Text, nullable=True)

    galaxy: Mapped["Galaxy"] = relationship(back_populates="planets")
    artifact: Mapped["Artifact | None"] = relationship(back_populates="planet")
    discoveries: Mapped[list["Discovery"]] = relationship(
        back_populates="planet",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Discovery.order_number",
    )
    practice_challenges: Mapped[list["PracticeChallenge"]] = relationship(
        back_populates="planet",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="PracticeChallenge.order_number",
    )
    quiz_questions: Mapped[list["QuizQuestion"]] = relationship(
        back_populates="planet",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="QuizQuestion.order_number",
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        back_populates="planet",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    user_progress_entries: Mapped[list["UserProgress"]] = relationship(
        back_populates="planet",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
