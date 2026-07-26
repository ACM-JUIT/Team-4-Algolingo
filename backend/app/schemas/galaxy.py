from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.base import UUIDTimestampedReadSchema, ORMBaseSchema


class GalaxySummary(ORMBaseSchema):
    id: UUID
    name: str
    description: str | None = None
    programming_language: str | None = None
    order_number: int = Field(ge=1)
    is_locked: bool
    icon_url: str | None = None


class GalaxyExplorerItem(GalaxySummary):
    total_planets: int = Field(default=0, ge=0)
    completed_planets: int = Field(default=0, ge=0)
    progress_percent: float = Field(default=0, ge=0, le=100)


class GalaxyDetail(UUIDTimestampedReadSchema):
    name: str
    description: str | None = None
    programming_language: str | None = None
    order_number: int = Field(ge=1)
    is_locked: bool
    icon_url: str | None = None
    planets: list["PlanetExplorerCard"] = Field(default_factory=list)


from app.schemas.planet import PlanetExplorerCard

GalaxyDetail.model_rebuild()
