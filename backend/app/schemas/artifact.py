from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import UUIDTimestampedReadSchema, ORMBaseSchema
from app.schemas.enums import ArtifactCategoryEnum, ArtifactRarityEnum


class ArtifactSummary(ORMBaseSchema):
    id: UUID
    name: str
    rarity: ArtifactRarityEnum
    category: ArtifactCategoryEnum
    xp_bonus_percent: int = Field(ge=0)
    icon_url: str | None = None
    is_hidden: bool = False


class ArtifactRead(UUIDTimestampedReadSchema):
    name: str
    description: str | None = None
    rarity: ArtifactRarityEnum
    rarity_color: str | None = None
    category: ArtifactCategoryEnum
    unlock_condition: str | None = None
    xp_bonus_percent: int = Field(ge=0)
    icon_url: str | None = None
    display_order: int = Field(ge=0)
    is_hidden: bool = False


class UserArtifactRead(ORMBaseSchema):
    id: UUID
    user_id: UUID
    artifact_id: UUID
    showcased: bool = False
    unlocked_at: datetime
    artifact: ArtifactSummary


class ArtifactCollectionItem(ORMBaseSchema):
    artifact: ArtifactRead
    collected: bool = False
    showcased: bool = False
    unlocked_at: datetime | None = None


class ArtifactShowcaseUpdateRequest(ORMBaseSchema):
    showcased: bool
