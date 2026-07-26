from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, extra="forbid")


class UUIDReadSchema(ORMBaseSchema):
    id: UUID


class TimestampedReadSchema(ORMBaseSchema):
    created_at: datetime
    updated_at: datetime


class UUIDTimestampedReadSchema(UUIDReadSchema, TimestampedReadSchema):
    pass
