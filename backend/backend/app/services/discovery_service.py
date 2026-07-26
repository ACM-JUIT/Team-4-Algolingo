from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.discovery import Discovery
from app.schemas.discovery import DiscoveryRead, DiscoverySummary
from app.services.service_utils import ensure_string_list


class DiscoveryService:
    @staticmethod
    def serialize_discovery(discovery: Discovery, status_override: str | None = None) -> DiscoveryRead:
        return DiscoveryRead(
            id=discovery.id,
            planet_id=discovery.planet_id,
            title=discovery.title,
            description=discovery.description,
            content_md=discovery.content_md,
            learning_objective=discovery.learning_objective,
            read_time_minutes=discovery.read_time_minutes,
            difficulty=discovery.difficulty,
            xp_reward=discovery.xp_reward,
            order_number=discovery.order_number,
            status=status_override or discovery.status,
            prerequisites=ensure_string_list(discovery.prerequisites),
            created_at=discovery.created_at,
            updated_at=discovery.updated_at,
        )

    @staticmethod
    def serialize_summary(discovery: Discovery, status_override: str | None = None) -> DiscoverySummary:
        return DiscoverySummary(
            id=discovery.id,
            planet_id=discovery.planet_id,
            title=discovery.title,
            description=discovery.description,
            learning_objective=discovery.learning_objective,
            read_time_minutes=discovery.read_time_minutes,
            difficulty=discovery.difficulty,
            xp_reward=discovery.xp_reward,
            order_number=discovery.order_number,
            status=status_override or discovery.status,
            prerequisites=ensure_string_list(discovery.prerequisites),
        )

    @classmethod
    async def get_discovery(cls, session: AsyncSession, discovery_id: UUID) -> DiscoveryRead:
        discovery = await session.get(Discovery, discovery_id)
        if discovery is None:
            raise AppException(message="Discovery not found", status_code=404)
        return cls.serialize_discovery(discovery)

    @classmethod
    async def list_planet_discoveries(cls, session: AsyncSession, planet_id: UUID) -> list[DiscoverySummary]:
        result = await session.execute(
            select(Discovery)
            .where(Discovery.planet_id == planet_id)
            .order_by(Discovery.order_number.asc())
        )
        return [cls.serialize_summary(discovery) for discovery in result.scalars().all()]
