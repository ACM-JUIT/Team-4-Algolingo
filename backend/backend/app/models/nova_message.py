from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin
from app.models.enums import JSONPayload, NovaSender, build_sa_enum


class NovaMessage(UUIDPrimaryKeyMixin, Base):
    """Represents a persisted NOVA chat message."""

    __tablename__ = "nova_messages"

    session_id: Mapped[UUID] = mapped_column(ForeignKey("nova_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    sender: Mapped[NovaSender] = mapped_column(
        build_sa_enum(NovaSender, name="nova_sender_enum", length=20),
        nullable=False,
        default=NovaSender.USER,
        server_default=text("'user'"),
        index=True,
    )
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    context_data: Mapped[JSONPayload | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())

    session: Mapped["NovaSession"] = relationship(back_populates="messages")
