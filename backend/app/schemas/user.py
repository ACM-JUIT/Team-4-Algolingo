from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr, Field

from app.schemas.base import ORMBaseSchema, UUIDTimestampedReadSchema
from app.schemas.enums import RankTitleEnum, UserRoleEnum, UserStatusEnum


class UserRead(UUIDTimestampedReadSchema):
    username: str
    email: EmailStr
    avatar_url: str | None = None
    bio: str | None = None
    xp: int
    level: int
    rank_title: RankTitleEnum
    streak_days: int
    last_login_date: date | None = None
    status: UserStatusEnum
    role: UserRoleEnum


class UserPublicProfile(ORMBaseSchema):
    id: UUID
    username: str
    avatar_url: str | None = None
    bio: str | None = None
    xp: int
    level: int
    rank_title: RankTitleEnum
    streak_days: int
    created_at: datetime


class UserProfileUpdateRequest(ORMBaseSchema):
    avatar_url: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=500)


class UserProfileStats(ORMBaseSchema):
    completed_planets: int = Field(default=0, ge=0)
    completed_discoveries: int = Field(default=0, ge=0)
    completed_practices: int = Field(default=0, ge=0)
    quizzes_passed: int = Field(default=0, ge=0)
    artifacts_earned: int = Field(default=0, ge=0)


class UserProfileRead(ORMBaseSchema):
    user: UserPublicProfile
    stats: UserProfileStats
