from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin


class DailyLogin(UUIDPrimaryKeyMixin, Base):
    """Represents a recorded daily login reward for a user."""

    __tablename__ = "daily_logins"
    __table_args__ = (
        UniqueConstraint("user_id", "login_date", name="uq_daily_logins_user_date"),
        CheckConstraint("xp_earned >= 0", name="daily_logins_xp_earned_non_negative"),
        CheckConstraint("streak_day >= 1", name="daily_logins_streak_day_minimum"),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    login_date: Mapped[date] = mapped_column(Date, nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=25, server_default=text("25"))
    streak_day: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"] = relationship(back_populates="daily_logins")
