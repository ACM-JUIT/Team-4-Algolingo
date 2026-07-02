from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import EventType
from app.models.user_event import UserEvent
from app.schemas.event import UserEventRead


class EventService:
    """Provides lightweight analytics event persistence helpers."""

    @staticmethod
    def normalize_event_data(event_data: dict[str, Any] | list[Any] | None) -> dict[str, Any] | list[Any] | None:
        """Normalizes event payloads before writing them to JSONB."""
        if event_data is None:
            return None
        if isinstance(event_data, (dict, list)):
            return event_data
        return {"value": str(event_data)}

    @classmethod
    async def track_event(
        cls,
        session: AsyncSession,
        *,
        user_id: UUID,
        event_type: EventType | str,
        event_data: dict[str, Any] | list[Any] | None = None,
        commit: bool = False,
    ) -> UserEventRead:
        """Persists a user event and optionally commits the session."""
        normalized_event_type = event_type if isinstance(event_type, EventType) else EventType(event_type)
        event = UserEvent(
            user_id=user_id,
            event_type=normalized_event_type,
            event_data=cls.normalize_event_data(event_data),
        )
        session.add(event)
        await session.flush()

        if commit:
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            await session.refresh(event)

        return UserEventRead.model_validate(event)

    @staticmethod
    async def list_recent_events(
        session: AsyncSession,
        *,
        user_id: UUID,
        limit: int = 5,
    ) -> list[UserEventRead]:
        """Returns recent user activity ordered from newest to oldest."""
        result = await session.execute(
            select(UserEvent)
            .where(UserEvent.user_id == user_id)
            .order_by(UserEvent.created_at.desc())
            .limit(limit)
        )
        return [UserEventRead.model_validate(event) for event in result.scalars().all()]
