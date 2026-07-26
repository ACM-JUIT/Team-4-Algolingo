from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin


class UserArtifact(UUIDPrimaryKeyMixin, Base):
    """Represents an artifact collected by a user."""

    __tablename__ = "user_artifacts"
    __table_args__ = (
        UniqueConstraint("user_id", "artifact_id", name="uq_user_artifacts_user_artifact"),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    artifact_id: Mapped[UUID] = mapped_column(ForeignKey("artifacts.id", ondelete="CASCADE"), nullable=False, index=True)
    showcased: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))
    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="user_artifacts")
    artifact: Mapped["Artifact"] = relationship(back_populates="user_artifacts")
