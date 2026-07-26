from __future__ import annotations

from sqlalchemy import Boolean, CheckConstraint, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ArtifactCategory, ArtifactRarity, build_sa_enum


class Artifact(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents a collectible achievement artifact."""

    __tablename__ = "artifacts"
    __table_args__ = (
        CheckConstraint("xp_bonus_percent >= 0", name="artifacts_xp_bonus_non_negative"),
        CheckConstraint("display_order >= 0", name="artifacts_display_order_non_negative"),
        CheckConstraint("char_length(name) >= 1", name="artifacts_name_min_length"),
    )

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    rarity: Mapped[ArtifactRarity] = mapped_column(
        build_sa_enum(ArtifactRarity, name="artifact_rarity_enum", length=20),
        nullable=False,
        index=True,
    )
    rarity_color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    category: Mapped[ArtifactCategory] = mapped_column(
        build_sa_enum(ArtifactCategory, name="artifact_category_enum", length=50),
        nullable=False,
        index=True,
    )
    unlock_condition: Mapped[str | None] = mapped_column(Text, nullable=True)
    xp_bonus_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))

    planet: Mapped["Planet | None"] = relationship(back_populates="artifact", uselist=False)
    user_artifacts: Mapped[list["UserArtifact"]] = relationship(
        back_populates="artifact",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
