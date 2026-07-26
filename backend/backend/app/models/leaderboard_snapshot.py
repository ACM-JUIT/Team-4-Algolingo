from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import LeaderboardType, build_sa_enum


class LeaderboardSnapshot(UUIDPrimaryKeyMixin, Base):
    """Represents a stored leaderboard snapshot for a user."""

    __tablename__ = "leaderboard_snapshots"
    __table_args__ = (
        CheckConstraint("rank_position >= 1", name="leaderboard_snapshots_rank_position_minimum"),
        CheckConstraint("xp >= 0", name="leaderboard_snapshots_xp_non_negative"),
        Index(
            "ix_leaderboard_snapshots_type_date_rank",
            "leaderboard_type",
            "snapshot_date",
            "rank_position",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    leaderboard_type: Mapped[LeaderboardType] = mapped_column(
        build_sa_enum(LeaderboardType, name="leaderboard_type_enum", length=20),
        nullable=False,
        index=True,
    )
    rank_position: Mapped[int] = mapped_column(Integer, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="leaderboard_snapshots")
