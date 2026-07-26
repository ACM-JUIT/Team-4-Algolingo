from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.models.galaxy import Galaxy
from app.models.planet import Planet
from app.models.user import User
from app.models.user_artifact import UserArtifact
from app.models.user_progress import UserProgress
from app.schemas.dashboard import ContinueLearningCard, DashboardQuickStats, DashboardRead
from app.schemas.user import UserRead
from app.services.event_service import EventService
from app.services.service_utils import calculate_percentage, ensure_string_list
from app.services.user_service import UserService


class DashboardService:
    @staticmethod
    def leaderboard_is_unlocked(*, level: int, completed_planets: int) -> bool:
        return level >= 3 and completed_planets >= 1

    @staticmethod
    def build_continue_learning_card(
        *,
        galaxy: Galaxy,
        planet: Planet,
        progress: UserProgress | None,
        next_discovery_id: UUID | None,
        next_practice_id: UUID | None,
    ) -> ContinueLearningCard:
        completed_discoveries = len(ensure_string_list(progress.completed_discoveries)) if progress else 0
        completed_practices = len(ensure_string_list(progress.completed_practices)) if progress else 0
        total_units = len(planet.discoveries) + len(planet.practice_challenges) + 1
        completed_units = completed_discoveries + completed_practices + (1 if progress and progress.quiz_passed else 0)

        return ContinueLearningCard(
            galaxy_id=galaxy.id,
            galaxy_name=galaxy.name,
            planet_id=planet.id,
            planet_name=planet.name,
            next_discovery_id=next_discovery_id,
            next_practice_id=next_practice_id,
            progress_percent=calculate_percentage(completed_units, total_units),
        )

    @staticmethod
    def select_next_discovery(planet: Planet, progress: UserProgress | None) -> UUID | None:
        completed_ids = set(ensure_string_list(progress.completed_discoveries) if progress else [])
        for discovery in sorted(planet.discoveries, key=lambda item: item.order_number):
            if str(discovery.id) not in completed_ids:
                return discovery.id
        return None

    @staticmethod
    def select_next_practice(planet: Planet, progress: UserProgress | None) -> UUID | None:
        completed_ids = set(ensure_string_list(progress.completed_practices) if progress else [])
        for practice in sorted(planet.practice_challenges, key=lambda item: item.order_number):
            if str(practice.id) not in completed_ids:
                return practice.id
        return None

    @classmethod
    def choose_continue_learning(
        cls,
        *,
        galaxies: list[Galaxy],
        progress_map: dict[UUID, UserProgress],
    ) -> ContinueLearningCard | None:
        ordered_galaxies = sorted(galaxies, key=lambda item: item.order_number)
        for galaxy in ordered_galaxies:
            for planet in sorted(galaxy.planets, key=lambda item: item.order_number):
                progress = progress_map.get(planet.id)
                if progress and progress.completed:
                    continue
                return cls.build_continue_learning_card(
                    galaxy=galaxy,
                    planet=planet,
                    progress=progress,
                    next_discovery_id=cls.select_next_discovery(planet, progress),
                    next_practice_id=cls.select_next_practice(planet, progress),
                )
        return None

    @classmethod
    async def get_dashboard(cls, session: AsyncSession, user_id: UUID) -> DashboardRead:
        user = await session.get(User, user_id)
        if user is None:
            raise AppException(message="User not found", status_code=404)

        progress_result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
        progress_rows = progress_result.scalars().all()
        progress_map = {row.planet_id: row for row in progress_rows}

        artifact_result = await session.execute(select(UserArtifact).where(UserArtifact.user_id == user_id))
        artifact_rows = artifact_result.scalars().all()

        galaxies_result = await session.execute(
            select(Galaxy)
            .options(
                selectinload(Galaxy.planets).selectinload(Planet.discoveries),
                selectinload(Galaxy.planets).selectinload(Planet.practice_challenges),
            )
            .where(Galaxy.is_locked.is_(False))
            .order_by(Galaxy.order_number.asc())
        )
        galaxies = galaxies_result.scalars().unique().all()

        profile_stats = UserService.build_profile_stats(
            progress_rows=progress_rows,
            artifacts_count=len(artifact_rows),
        )
        recent_activity = await EventService.list_recent_events(session=session, user_id=user_id, limit=5)

        return DashboardRead(
            user=UserRead.model_validate(user),
            quick_stats=DashboardQuickStats(
                xp=user.xp,
                level=user.level,
                rank_title=user.rank_title,
                streak_days=user.streak_days,
                completed_planets=profile_stats.completed_planets,
                completed_discoveries=profile_stats.completed_discoveries,
                completed_practices=profile_stats.completed_practices,
                artifacts_earned=profile_stats.artifacts_earned,
            ),
            continue_learning=cls.choose_continue_learning(galaxies=galaxies, progress_map=progress_map),
            recent_activity=recent_activity,
            leaderboard_unlocked=cls.leaderboard_is_unlocked(
                level=user.level,
                completed_planets=profile_stats.completed_planets,
            ),
        )
