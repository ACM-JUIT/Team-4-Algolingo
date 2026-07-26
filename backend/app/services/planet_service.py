from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.models.planet import Planet
from app.models.quiz_attempt import QuizAttempt
from app.models.user_progress import UserProgress
from app.schemas.artifact import ArtifactSummary
from app.schemas.enums import PlanetStatusEnum
from app.schemas.planet import PlanetDetail, PlanetExplorerCard, PlanetProgressSummary
from app.services.discovery_service import DiscoveryService
from app.services.practice_service import PracticeService
from app.services.progress_service import ProgressService
from app.services.quiz_service import QuizService
from app.services.service_utils import calculate_percentage, ensure_string_list


class PlanetService:
    @staticmethod
    def calculate_planet_progress_percent(
        *,
        completed_discoveries_count: int,
        total_discoveries: int,
        completed_practices_count: int,
        total_practices: int,
        quiz_passed: bool,
    ) -> float:
        total_units = total_discoveries + total_practices + 1
        completed_units = completed_discoveries_count + completed_practices_count + (1 if quiz_passed else 0)
        return calculate_percentage(completed_units, total_units)

    @classmethod
    def build_progress_summary(
        cls,
        *,
        user_id: UUID,
        planet: Planet,
        progress: UserProgress | None,
        attempts_count: int,
        planet_status: PlanetStatusEnum = PlanetStatusEnum.UNLOCKED,
    ) -> PlanetProgressSummary:
        completed_discoveries_count = len(ensure_string_list(progress.completed_discoveries)) if progress else 0
        completed_practices_count = len(ensure_string_list(progress.completed_practices)) if progress else 0
        quiz_passed = bool(progress.quiz_passed) if progress else False

        quiz_status = ProgressService.determine_quiz_status(
            planet=planet,
            progress=progress,
            attempts_count=attempts_count,
            planet_status=planet_status,
        )

        return PlanetProgressSummary(
            user_id=user_id,
            planet_id=planet.id,
            status=PlanetStatusEnum.COMPLETED if progress and progress.completed else planet_status,
            completed_discoveries_count=completed_discoveries_count,
            total_discoveries=len(planet.discoveries),
            completed_practices_count=completed_practices_count,
            total_practices=len(planet.practice_challenges),
            quiz_status=quiz_status,
            quiz_best_score=progress.quiz_best_score if progress else None,
            completed=bool(progress.completed) if progress else False,
            xp_earned=progress.xp_earned if progress else 0,
            started_at=progress.started_at if progress else None,
            completed_at=progress.completed_at if progress else None,
            last_activity_at=progress.last_activity_at if progress else None,
            progress_percent=cls.calculate_planet_progress_percent(
                completed_discoveries_count=completed_discoveries_count,
                total_discoveries=len(planet.discoveries),
                completed_practices_count=completed_practices_count,
                total_practices=len(planet.practice_challenges),
                quiz_passed=quiz_passed,
            ),
        )

    @classmethod
    def build_planet_explorer_card(
        cls,
        *,
        planet: Planet,
        progress: UserProgress | None,
        planet_status: PlanetStatusEnum,
    ) -> PlanetExplorerCard:
        completed_discoveries_count = len(ensure_string_list(progress.completed_discoveries)) if progress else 0
        completed_practices_count = len(ensure_string_list(progress.completed_practices)) if progress else 0
        quiz_passed = bool(progress.quiz_passed) if progress else False

        return PlanetExplorerCard(
            id=planet.id,
            galaxy_id=planet.galaxy_id,
            artifact_id=planet.artifact_id,
            name=planet.name,
            tagline=planet.tagline,
            description=planet.description,
            difficulty=planet.difficulty,
            order_number=planet.order_number,
            xp_total=planet.xp_total,
            estimated_time_minutes=planet.estimated_time_minutes,
            status=PlanetStatusEnum.COMPLETED if progress and progress.completed else planet_status,
            unlock_condition=planet.unlock_condition,
            discoveries_count=len(planet.discoveries),
            practices_count=len(planet.practice_challenges),
            quiz_questions_count=len(planet.quiz_questions),
            completed=bool(progress.completed) if progress else False,
            progress_percent=cls.calculate_planet_progress_percent(
                completed_discoveries_count=completed_discoveries_count,
                total_discoveries=len(planet.discoveries),
                completed_practices_count=completed_practices_count,
                total_practices=len(planet.practice_challenges),
                quiz_passed=quiz_passed,
            ),
        )

    @classmethod
    async def get_planet_detail(
        cls,
        session: AsyncSession,
        *,
        planet_id: UUID,
        user_id: UUID | None = None,
    ) -> PlanetDetail:
        result = await session.execute(
            select(Planet)
            .options(
                selectinload(Planet.galaxy),
                selectinload(Planet.discoveries),
                selectinload(Planet.practice_challenges),
                selectinload(Planet.quiz_questions),
                selectinload(Planet.artifact),
            )
            .where(Planet.id == planet_id)
        )
        planet = result.scalar_one_or_none()
        if planet is None:
            raise AppException(message="Planet not found", status_code=404)

        progress = None
        attempts_count = 0
        planet_status = PlanetStatusEnum.UNLOCKED if not planet.galaxy.is_locked else PlanetStatusEnum.LOCKED
        if user_id is not None:
            all_planets_result = await session.execute(
                select(Planet)
                .where(Planet.galaxy_id == planet.galaxy_id)
                .order_by(Planet.order_number.asc())
            )
            all_planets = all_planets_result.scalars().all()
            progress_result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
            progress_map = {row.planet_id: row for row in progress_result.scalars().all()}
            progress = progress_map.get(planet.id)
            planet_status_map = ProgressService.build_planet_status_map(
                planets=all_planets,
                progress_map=progress_map,
                galaxy_locked=planet.galaxy.is_locked,
            )
            planet_status = planet_status_map.get(planet.id, PlanetStatusEnum.LOCKED)

            attempts_count_result = await session.execute(
                select(func.count(QuizAttempt.id)).where(
                    QuizAttempt.user_id == user_id,
                    QuizAttempt.planet_id == planet.id,
                )
            )
            attempts_count = int(attempts_count_result.scalar_one() or 0)
        else:
            progress_map = {}

        completed_discovery_ids = set(ensure_string_list(progress.completed_discoveries)) if progress else set()
        completed_practice_ids = set(ensure_string_list(progress.completed_practices)) if progress else set()

        return PlanetDetail(
            id=planet.id,
            galaxy_id=planet.galaxy_id,
            artifact_id=planet.artifact_id,
            name=planet.name,
            tagline=planet.tagline,
            description=planet.description,
            difficulty=planet.difficulty,
            order_number=planet.order_number,
            xp_total=planet.xp_total,
            estimated_time_minutes=planet.estimated_time_minutes,
            status=PlanetStatusEnum.COMPLETED if progress and progress.completed else planet_status,
            unlock_condition=planet.unlock_condition,
            created_at=planet.created_at,
            updated_at=planet.updated_at,
            discoveries=[
                DiscoveryService.serialize_summary(
                    item,
                    status_override=ProgressService.determine_discovery_status(
                        discovery=item,
                        planet=planet,
                        completed_discovery_ids=completed_discovery_ids,
                        planet_status=planet_status,
                    ).value,
                )
                for item in sorted(planet.discoveries, key=lambda item: item.order_number)
            ],
            practice_challenges=[
                PracticeService.serialize_summary(
                    item,
                    status_override=ProgressService.determine_practice_status(
                        practice=item,
                        planet=planet,
                        completed_practice_ids=completed_practice_ids,
                        planet_status=planet_status,
                    ).value,
                )
                for item in sorted(planet.practice_challenges, key=lambda item: item.order_number)
            ],
            quiz=await QuizService.get_quiz_overview(
                session=session,
                planet=planet,
                user_id=user_id,
                progress=progress,
            ),
            artifact=(
                None
                if planet.artifact is None
                else ArtifactSummary(
                    id=planet.artifact.id,
                    name=planet.artifact.name,
                    rarity=planet.artifact.rarity,
                    category=planet.artifact.category,
                    xp_bonus_percent=planet.artifact.xp_bonus_percent,
                    icon_url=planet.artifact.icon_url,
                    is_hidden=planet.artifact.is_hidden,
                )
            ),
            progress=(
                None
                if user_id is None
                else cls.build_progress_summary(
                    user_id=user_id,
                    planet=planet,
                    progress=progress,
                    attempts_count=attempts_count,
                    planet_status=planet_status,
                )
            ),
        )
