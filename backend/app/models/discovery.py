from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DiscoveryStatus, JSONStringList, build_sa_enum


class Discovery(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a lesson discovery within a planet."""

    __tablename__ = "discoveries"
    __table_args__ = (
        UniqueConstraint("planet_id", "order_number", name="uq_discoveries_planet_order_number"),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="discoveries_difficulty_range"),
        CheckConstraint("xp_reward >= 0", name="discoveries_xp_reward_non_negative"),
        CheckConstraint(
            "read_time_minutes IS NULL OR read_time_minutes >= 0",
            name="discoveries_read_time_non_negative",
        ),
        CheckConstraint("char_length(title) >= 1", name="discoveries_title_min_length"),
    )

    planet_id: Mapped[UUID] = mapped_column(ForeignKey("planets.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_objective: Mapped[str | None] = mapped_column(Text, nullable=True)
    read_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[DiscoveryStatus] = mapped_column(
        build_sa_enum(DiscoveryStatus, name="discovery_status_enum", length=20),
        nullable=False,
        default=DiscoveryStatus.LOCKED,
        server_default=text("'LOCKED'"),
        index=True,
    )
    prerequisites: Mapped[JSONStringList] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    planet: Mapped["Planet"] = relationship(back_populates="discoveries")
