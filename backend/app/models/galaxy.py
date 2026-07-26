from __future__ import annotations

from sqlalchemy import Boolean, CheckConstraint, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Galaxy(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a programming language galaxy."""

    __tablename__ = "galaxies"
    __table_args__ = (
        CheckConstraint("order_number >= 1", name="galaxies_order_number_minimum"),
        CheckConstraint("char_length(name) >= 1", name="galaxies_name_min_length"),
    )

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    programming_language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    order_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("true"))
    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    planets: Mapped[list["Planet"]] = relationship(
        back_populates="galaxy",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Planet.order_number",
    )
