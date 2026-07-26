from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import ORMBaseSchema, UUIDTimestampedReadSchema
from app.schemas.enums import PlanetStatusEnum, QuizStatusEnum


class PlanetSummary(ORMBaseSchema):
    id: UUID
    galaxy_id: UUID
    artifact_id: UUID | None = None
    name: str
    tagline: str | None = None
    description: str | None = None
    difficulty: int = Field(ge=1, le=5)
    order_number: int = Field(ge=1)
    xp_total: int = Field(ge=0)
    estimated_time_minutes: int | None = Field(default=None, ge=0)
    status: PlanetStatusEnum
    unlock_condition: str | None = None


class PlanetExplorerCard(PlanetSummary):
    discoveries_count: int = Field(default=0, ge=0)
    practices_count: int = Field(default=0, ge=0)
    quiz_questions_count: int = Field(default=0, ge=0)
    completed: bool = False
    progress_percent: float = Field(default=0, ge=0, le=100)


class PlanetProgressSummary(ORMBaseSchema):
    user_id: UUID
    planet_id: UUID
    status: PlanetStatusEnum
    completed_discoveries_count: int = Field(default=0, ge=0)
    total_discoveries: int = Field(default=0, ge=0)
    completed_practices_count: int = Field(default=0, ge=0)
    total_practices: int = Field(default=0, ge=0)
    quiz_status: QuizStatusEnum
    quiz_best_score: int | None = Field(default=None, ge=0)
    completed: bool = False
    xp_earned: int = Field(default=0, ge=0)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    last_activity_at: datetime | None = None
    progress_percent: float = Field(default=0, ge=0, le=100)


class PlanetDetail(UUIDTimestampedReadSchema):
    galaxy_id: UUID
    artifact_id: UUID | None = None
    name: str
    tagline: str | None = None
    description: str | None = None
    difficulty: int = Field(ge=1, le=5)
    order_number: int = Field(ge=1)
    xp_total: int = Field(ge=0)
    estimated_time_minutes: int | None = Field(default=None, ge=0)
    status: PlanetStatusEnum
    unlock_condition: str | None = None
    discoveries: list["DiscoverySummary"] = Field(default_factory=list)
    practice_challenges: list["PracticeChallengeSummary"] = Field(default_factory=list)
    quiz: "QuizOverview | None" = None
    artifact: "ArtifactSummary | None" = None
    progress: PlanetProgressSummary | None = None


from app.schemas.artifact import ArtifactSummary
from app.schemas.discovery import DiscoverySummary
from app.schemas.practice import PracticeChallengeSummary
from app.schemas.quiz import QuizOverview

PlanetDetail.model_rebuild()
