from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import Field

from app.schemas.base import ORMBaseSchema
from app.schemas.enums import LeaderboardTypeEnum, RankTitleEnum


class LeaderboardQueryParams(ORMBaseSchema):
    type: LeaderboardTypeEnum = LeaderboardTypeEnum.GLOBAL
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=50)
    galaxy_id: UUID | None = None


class LeaderboardEntry(ORMBaseSchema):
    position: int = Field(ge=1)
    user_id: UUID
    username: str
    avatar_url: str | None = None
    xp: int = Field(ge=0)
    level: int = Field(ge=1)
    rank_title: RankTitleEnum


class UserLeaderboardPosition(ORMBaseSchema):
    leaderboard_type: LeaderboardTypeEnum
    position: int = Field(ge=1)
    xp: int = Field(ge=0)


class LeaderboardRead(ORMBaseSchema):
    leaderboard_type: LeaderboardTypeEnum
    items: list[LeaderboardEntry] = Field(default_factory=list)
    page: int = Field(ge=1)
    limit: int = Field(ge=1, le=50)
    total: int = Field(ge=0)
    snapshot_date: date | None = None
    user_position: UserLeaderboardPosition | None = None
