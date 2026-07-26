from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import EventType, JSONPayload, build_sa_enum


class UserEvent(UUIDPrimaryKeyMixin, Base):
    """Represents an analytics event emitted by a user action."""

    __tablename__ = "user_events"
    __table_args__ = (
        Index("ix_user_events_user_type_created", "user_id", "event_type", "created_at"),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type: Mapped[EventType] = mapped_column(
        build_sa_enum(EventType, name="event_type_enum", length=100),
        nullable=False,
        index=True,
    )
    event_data: Mapped[JSONPayload | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="user_events")
