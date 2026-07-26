from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.base import ORMBaseSchema, UUIDTimestampedReadSchema
from app.schemas.enums import DiscoveryStatusEnum, PlanetStatusEnum


class DiscoverySummary(ORMBaseSchema):
    id: UUID
    planet_id: UUID
    title: str
    description: str | None = None
    learning_objective: str | None = None
    read_time_minutes: int | None = Field(default=None, ge=0)
    difficulty: int = Field(ge=1, le=5)
    xp_reward: int = Field(ge=0)
    order_number: int = Field(ge=1)
    status: DiscoveryStatusEnum
    prerequisites: list[str] = Field(default_factory=list)


class DiscoveryRead(UUIDTimestampedReadSchema):
    planet_id: UUID
    title: str
    description: str | None = None
    content_md: str | None = None
    learning_objective: str | None = None
    read_time_minutes: int | None = Field(default=None, ge=0)
    difficulty: int = Field(ge=1, le=5)
    xp_reward: int = Field(ge=0)
    order_number: int = Field(ge=1)
    status: DiscoveryStatusEnum
    prerequisites: list[str] = Field(default_factory=list)


class DiscoveryCompletionResult(ORMBaseSchema):
    discovery_id: UUID
    planet_id: UUID
    completed: bool = True
    xp_awarded: int = Field(ge=0)
    total_completed_discoveries: int = Field(ge=0)
    planet_status: PlanetStatusEnum | None = None
