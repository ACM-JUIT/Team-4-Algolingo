from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.models.galaxy import Galaxy
from app.models.planet import Planet
from app.models.user_progress import UserProgress
from app.schemas.galaxy import GalaxyDetail, GalaxyExplorerItem
from app.services.planet_service import PlanetService
from app.services.progress_service import ProgressService
from app.services.service_utils import calculate_percentage


class GalaxyService:
    @staticmethod
    def calculate_progress_percent(*, completed_planets: int, total_planets: int) -> float:
        return calculate_percentage(completed_planets, total_planets)

    @classmethod
    async def list_galaxies(
        cls,
        session: AsyncSession,
        *,
        user_id: UUID | None = None,
    ) -> list[GalaxyExplorerItem]:
        result = await session.execute(
            select(Galaxy)
            .options(
                selectinload(Galaxy.planets).selectinload(Planet.discoveries),
                selectinload(Galaxy.planets).selectinload(Planet.practice_challenges),
                selectinload(Galaxy.planets).selectinload(Planet.quiz_questions),
            )
            .order_by(Galaxy.order_number.asc())
        )
        galaxies = result.scalars().unique().all()

        progress_map: dict[UUID, UserProgress] = {}
        if user_id is not None:
            progress_result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
            progress_map = {row.planet_id: row for row in progress_result.scalars().all()}

        items: list[GalaxyExplorerItem] = []
        for galaxy in galaxies:
            completed_planets = sum(
                1 for planet in galaxy.planets if progress_map.get(planet.id) and progress_map[planet.id].completed
            )
            items.append(
                GalaxyExplorerItem(
                    id=galaxy.id,
                    name=galaxy.name,
                    description=galaxy.description,
                    programming_language=galaxy.programming_language,
                    order_number=galaxy.order_number,
                    is_locked=galaxy.is_locked,
                    icon_url=galaxy.icon_url,
                    total_planets=len(galaxy.planets),
                    completed_planets=completed_planets,
                    progress_percent=cls.calculate_progress_percent(
                        completed_planets=completed_planets,
                        total_planets=len(galaxy.planets),
                    ),
                )
            )
        return items

    @classmethod
    async def get_galaxy_detail(
        cls,
        session: AsyncSession,
        *,
        galaxy_id: UUID,
        user_id: UUID | None = None,
    ) -> GalaxyDetail:
        result = await session.execute(
            select(Galaxy)
            .options(
                selectinload(Galaxy.planets).selectinload(Planet.discoveries),
                selectinload(Galaxy.planets).selectinload(Planet.practice_challenges),
                selectinload(Galaxy.planets).selectinload(Planet.quiz_questions),
            )
            .where(Galaxy.id == galaxy_id)
        )
        galaxy = result.scalar_one_or_none()
        if galaxy is None:
            raise AppException(message="Galaxy not found", status_code=404)

        progress_map: dict[UUID, UserProgress] = {}
        if user_id is not None:
            progress_result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
            progress_map = {row.planet_id: row for row in progress_result.scalars().all()}

        planet_status_map = ProgressService.build_planet_status_map(
            planets=galaxy.planets,
            progress_map=progress_map,
            galaxy_locked=galaxy.is_locked,
        )

        return GalaxyDetail(
            id=galaxy.id,
            name=galaxy.name,
            description=galaxy.description,
            programming_language=galaxy.programming_language,
            order_number=galaxy.order_number,
            is_locked=galaxy.is_locked,
            icon_url=galaxy.icon_url,
            created_at=galaxy.created_at,
            updated_at=galaxy.updated_at,
            planets=[
                PlanetService.build_planet_explorer_card(
                    planet=planet,
                    progress=progress_map.get(planet.id),
                    planet_status=planet_status_map.get(planet.id),
                )
                for planet in sorted(galaxy.planets, key=lambda item: item.order_number)
            ],
        )
