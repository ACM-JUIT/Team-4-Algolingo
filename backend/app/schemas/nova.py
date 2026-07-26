from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import ORMBaseSchema
from app.schemas.enums import NovaSenderEnum


class NovaContextReference(ORMBaseSchema):
    galaxy_id: UUID | None = None
    planet_id: UUID | None = None
    discovery_id: UUID | None = None
    practice_id: UUID | None = None


class NovaAskRequest(ORMBaseSchema):
    message: str = Field(min_length=1, max_length=4000)
    session_id: UUID | None = None
    galaxy_id: UUID | None = None
    planet_id: UUID | None = None
    discovery_id: UUID | None = None
    practice_id: UUID | None = None


class NovaHintRequest(ORMBaseSchema):
    current_code: str | None = Field(default=None, max_length=20000)
    specific_problem: str | None = Field(default=None, max_length=2000)
    session_id: UUID | None = None


class NovaDebugRequest(ORMBaseSchema):
    code: str = Field(min_length=1, max_length=20000)
    problem_description: str | None = Field(default=None, max_length=4000)
    session_id: UUID | None = None
    galaxy_id: UUID | None = None
    planet_id: UUID | None = None
    practice_id: UUID | None = None


class NovaRecommendRequest(ORMBaseSchema):
    session_id: UUID | None = None
    galaxy_id: UUID | None = None
    planet_id: UUID | None = None


class NovaMessageRead(ORMBaseSchema):
    id: UUID
    session_id: UUID
    sender: NovaSenderEnum
    message: str | None = None
    context_data: dict[str, object] | list[object] | None = None
    created_at: datetime


class NovaSessionRead(ORMBaseSchema):
    id: UUID
    user_id: UUID
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    messages: list[NovaMessageRead] = Field(default_factory=list)


class NovaResponseData(ORMBaseSchema):
    session_id: UUID
    reply: str
    messages: list[NovaMessageRead] = Field(default_factory=list)
