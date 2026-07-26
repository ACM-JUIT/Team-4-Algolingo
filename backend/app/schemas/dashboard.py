from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import ORMBaseSchema
from app.schemas.enums import EventTypeEnum, RankTitleEnum
from app.schemas.user import UserRead


class RecentActivityItem(ORMBaseSchema):
    event_type: EventTypeEnum
    event_data: dict[str, object] | list[object] | None = None
    created_at: datetime


class ContinueLearningCard(ORMBaseSchema):
    galaxy_id: UUID
    galaxy_name: str
    planet_id: UUID
    planet_name: str
    next_discovery_id: UUID | None = None
    next_practice_id: UUID | None = None
    progress_percent: float = Field(default=0, ge=0, le=100)


class DashboardQuickStats(ORMBaseSchema):
    xp: int = Field(ge=0)
    level: int = Field(ge=1)
    rank_title: RankTitleEnum
    streak_days: int = Field(ge=0)
    completed_planets: int = Field(default=0, ge=0)
    completed_discoveries: int = Field(default=0, ge=0)
    completed_practices: int = Field(default=0, ge=0)
    artifacts_earned: int = Field(default=0, ge=0)


class DashboardRead(ORMBaseSchema):
    user: UserRead
    quick_stats: DashboardQuickStats
    continue_learning: ContinueLearningCard | None = None
    recent_activity: list[RecentActivityItem] = Field(default_factory=list)
    leaderboard_unlocked: bool = False
