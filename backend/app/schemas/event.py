from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.schemas.base import ORMBaseSchema
from app.schemas.enums import EventTypeEnum


class UserEventRead(ORMBaseSchema):
    id: UUID
    user_id: UUID
    event_type: EventTypeEnum
    event_data: dict[str, object] | list[object] | None = None
    created_at: datetime
