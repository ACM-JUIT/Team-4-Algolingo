from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.models.discovery import Discovery
from app.models.enums import EventType, ProgressStatus
from app.models.planet import Planet
from app.models.practice_challenge import PracticeChallenge
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_question import QuizQuestion
from app.models.user import User
from app.models.user_progress import UserProgress
from app.schemas.artifact import ArtifactSummary
from app.schemas.discovery import DiscoveryCompletionResult
from app.schemas.enums import DiscoveryStatusEnum, PlanetStatusEnum, PracticeStatusEnum, QuizStatusEnum
from app.schemas.practice import PracticeSubmissionResult
from app.schemas.quiz import QuizSubmitResult
from app.services.artifact_service import ArtifactService
from app.services.event_service import EventService
from app.services.quiz_service import QuizService
from app.services.rank_service import RankService
from app.services.service_utils import ensure_string_list
from app.services.xp_service import PLANET_COMPLETION_BONUS_XP, XPService


class ProgressService:
    """Coordinates learner progression, XP awards, and unlock state changes."""

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC).replace(tzinfo=None)

    @staticmethod
    def _prerequisites_met(prerequisites: list[str], completed_ids: set[str]) -> bool:
        return all(prerequisite in completed_ids for prerequisite in prerequisites)

    @staticmethod
    def _current_planet_status_from_progress(progress: UserProgress | None, fallback: PlanetStatusEnum) -> PlanetStatusEnum:
        if progress is None:
            return fallback
        if progress.completed:
            return PlanetStatusEnum.COMPLETED
        return PlanetStatusEnum.IN_PROGRESS

    @staticmethod
    async def _commit_and_refresh(session: AsyncSession, *instances: object) -> None:
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise

        for instance in instances:
            await session.refresh(instance)

    @classmethod
    def build_planet_status_map(
        cls,
        *,
        planets: list[Planet],
        progress_map: dict[UUID, UserProgress],
        galaxy_locked: bool,
    ) -> dict[UUID, PlanetStatusEnum]:
        """Builds sequential planet availability for a user within a galaxy."""
        statuses: dict[UUID, PlanetStatusEnum] = {}
        previous_completed = False

        for index, planet in enumerate(sorted(planets, key=lambda item: item.order_number)):
            progress = progress_map.get(planet.id)
            if galaxy_locked:
                statuses[planet.id] = PlanetStatusEnum.LOCKED
            elif progress and progress.completed:
                statuses[planet.id] = PlanetStatusEnum.COMPLETED
                previous_completed = True
            elif progress:
                statuses[planet.id] = PlanetStatusEnum.IN_PROGRESS
                previous_completed = False
            elif index == 0 or previous_completed:
                statuses[planet.id] = PlanetStatusEnum.UNLOCKED
                previous_completed = False
            else:
                statuses[planet.id] = PlanetStatusEnum.LOCKED
                previous_completed = False
        return statuses

    @classmethod
    def determine_discovery_status(
        cls,
        *,
        discovery: Discovery,
        planet: Planet,
        completed_discovery_ids: set[str],
        planet_status: PlanetStatusEnum,
    ) -> DiscoveryStatusEnum:
        """Determines whether a discovery is locked, available, or completed."""
        if str(discovery.id) in completed_discovery_ids:
            return DiscoveryStatusEnum.COMPLETED
        if planet_status == PlanetStatusEnum.LOCKED:
            return DiscoveryStatusEnum.LOCKED

        for earlier_discovery in sorted(planet.discoveries, key=lambda item: item.order_number):
            if earlier_discovery.order_number >= discovery.order_number:
                break
            if str(earlier_discovery.id) not in completed_discovery_ids:
                return DiscoveryStatusEnum.LOCKED

        prerequisites = ensure_string_list(discovery.prerequisites)
        if not cls._prerequisites_met(prerequisites, completed_discovery_ids):
            return DiscoveryStatusEnum.LOCKED
        return DiscoveryStatusEnum.AVAILABLE

    @classmethod
    def determine_practice_status(
        cls,
        *,
        practice: PracticeChallenge,
        planet: Planet,
        completed_practice_ids: set[str],
        planet_status: PlanetStatusEnum,
    ) -> PracticeStatusEnum:
        """Determines whether a practice challenge is locked, available, or completed."""
        if str(practice.id) in completed_practice_ids:
            return PracticeStatusEnum.COMPLETED
        if planet_status == PlanetStatusEnum.LOCKED:
            return PracticeStatusEnum.LOCKED

        for earlier_practice in sorted(planet.practice_challenges, key=lambda item: item.order_number):
            if earlier_practice.order_number >= practice.order_number:
                break
            if str(earlier_practice.id) not in completed_practice_ids:
                return PracticeStatusEnum.LOCKED
        return PracticeStatusEnum.AVAILABLE

    @classmethod
    def determine_quiz_status(
        cls,
        *,
        planet: Planet,
        progress: UserProgress | None,
        attempts_count: int,
        planet_status: PlanetStatusEnum,
    ) -> QuizStatusEnum:
        """Determines the effective quiz state for a planet."""
        if planet_status == PlanetStatusEnum.LOCKED:
            return QuizStatusEnum.LOCKED

        completed_discovery_ids = set(ensure_string_list(progress.completed_discoveries)) if progress else set()
        completed_practice_ids = set(ensure_string_list(progress.completed_practices)) if progress else set()
        all_discoveries_completed = len(completed_discovery_ids) >= len(planet.discoveries) and len(planet.discoveries) > 0
        all_practices_completed = len(completed_practice_ids) >= len(planet.practice_challenges) and len(planet.practice_challenges) > 0
        return QuizService.determine_quiz_status(
            all_discoveries_completed=all_discoveries_completed,
            all_practices_completed=all_practices_completed,
            quiz_passed=bool(progress.quiz_passed) if progress else False,
            attempts_count=attempts_count,
        )

    @classmethod
    async def load_planet_with_content(cls, session: AsyncSession, planet_id: UUID) -> Planet:
        result = await session.execute(
            select(Planet)
            .options(
                selectinload(Planet.galaxy),
                selectinload(Planet.artifact),
                selectinload(Planet.discoveries),
                selectinload(Planet.practice_challenges),
                selectinload(Planet.quiz_questions),
            )
            .where(Planet.id == planet_id)
        )
        planet = result.scalar_one_or_none()
        if planet is None:
            raise AppException(message="Planet not found", status_code=404)
        return planet

    @classmethod
    async def get_or_create_progress(cls, session: AsyncSession, *, user_id: UUID, planet_id: UUID) -> UserProgress:
        """Returns an existing progress row or creates one for the user and planet."""
        result = await session.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.planet_id == planet_id,
            )
        )
        progress = result.scalar_one_or_none()
        if progress is not None:
            return progress

        progress = UserProgress(
            user_id=user_id,
            planet_id=planet_id,
            completed_discoveries=[],
            completed_practices=[],
            quiz_passed=False,
            completed=False,
            status=ProgressStatus.IN_PROGRESS.value,
            xp_earned=0,
            started_at=cls._now(),
            last_activity_at=cls._now(),
        )
        session.add(progress)
        await session.flush()
        return progress

    @classmethod
    async def ensure_planet_is_unlocked(cls, session: AsyncSession, *, user_id: UUID, planet: Planet) -> PlanetStatusEnum:
        """Ensures the requested planet is currently accessible to the learner."""
        galaxy_planets_result = await session.execute(
            select(Planet)
            .where(Planet.galaxy_id == planet.galaxy_id)
            .order_by(Planet.order_number.asc())
        )
        galaxy_planets = galaxy_planets_result.scalars().all()

        progress_result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
        progress_map = {row.planet_id: row for row in progress_result.scalars().all()}
        statuses = cls.build_planet_status_map(
            planets=galaxy_planets,
            progress_map=progress_map,
            galaxy_locked=bool(planet.galaxy.is_locked) if planet.galaxy is not None else False,
        )
        status = statuses.get(planet.id, PlanetStatusEnum.LOCKED)
        if status == PlanetStatusEnum.LOCKED:
            raise AppException(message="This planet is locked", status_code=403)
        return status

    @classmethod
    async def _update_planet_completion_if_eligible(
        cls,
        session: AsyncSession,
        *,
        user: User,
        planet: Planet,
        progress: UserProgress,
        bonus_percent_override: int,
    ) -> list[ArtifactSummary]:
        completed_discovery_ids = set(ensure_string_list(progress.completed_discoveries))
        completed_practice_ids = set(ensure_string_list(progress.completed_practices))
        is_complete = (
            len(completed_discovery_ids) >= len(planet.discoveries)
            and len(completed_practice_ids) >= len(planet.practice_challenges)
            and progress.quiz_passed
        )
        if not is_complete or progress.completed:
            return []

        progress.completed = True
        progress.status = ProgressStatus.COMPLETED.value
        progress.completed_at = cls._now()
        progress.last_activity_at = cls._now()

        award = await XPService.award_user_xp(
            session=session,
            user=user,
            base_xp=PLANET_COMPLETION_BONUS_XP,
            bonus_percent_override=bonus_percent_override,
        )
        progress.xp_earned += award.total_xp

        unlocked_artifact = await ArtifactService.unlock_planet_artifact(
            session=session,
            user=user,
            artifact=planet.artifact,
            bonus_percent_override=bonus_percent_override,
        )
        await EventService.track_event(
            session=session,
            user_id=user.id,
            event_type=EventType.PLANET_COMPLETED,
            event_data={
                "planet_id": str(planet.id),
                "planet_name": planet.name,
                "xp_awarded": award.total_xp,
            },
        )
        await RankService.sync_user_rank(session=session, user=user)
        return [] if unlocked_artifact is None else [unlocked_artifact]

    @classmethod
    async def complete_discovery(
        cls,
        session: AsyncSession,
        *,
        user: User,
        discovery_id: UUID,
    ) -> DiscoveryCompletionResult:
        """Marks a discovery complete and applies its progression rewards."""
        result = await session.execute(
            select(Discovery)
            .options(
                selectinload(Discovery.planet).selectinload(Planet.galaxy),
                selectinload(Discovery.planet).selectinload(Planet.discoveries),
                selectinload(Discovery.planet).selectinload(Planet.practice_challenges),
                selectinload(Discovery.planet).selectinload(Planet.quiz_questions),
            )
            .where(Discovery.id == discovery_id)
        )
        discovery = result.scalar_one_or_none()
        if discovery is None:
            raise AppException(message="Discovery not found", status_code=404)

        planet = discovery.planet
        planet_status = await cls.ensure_planet_is_unlocked(session=session, user_id=user.id, planet=planet)
        progress = await cls.get_or_create_progress(session=session, user_id=user.id, planet_id=planet.id)

        completed_discovery_ids = set(ensure_string_list(progress.completed_discoveries))
        status = cls.determine_discovery_status(
            discovery=discovery,
            planet=planet,
            completed_discovery_ids=completed_discovery_ids,
            planet_status=planet_status,
        )
        if status == DiscoveryStatusEnum.LOCKED:
            raise AppException(message="This discovery is locked", status_code=403)

        if status == DiscoveryStatusEnum.COMPLETED:
            return DiscoveryCompletionResult(
                discovery_id=discovery.id,
                planet_id=planet.id,
                completed=True,
                xp_awarded=0,
                total_completed_discoveries=len(completed_discovery_ids),
                planet_status=cls._current_planet_status_from_progress(progress, planet_status),
            )

        bonus_percent = await XPService.get_total_artifact_bonus_percent(session=session, user_id=user.id)
        completed_discovery_ids.add(str(discovery.id))
        progress.completed_discoveries = sorted(completed_discovery_ids)
        progress.status = ProgressStatus.IN_PROGRESS.value
        progress.last_activity_at = cls._now()

        award = await XPService.award_user_xp(
            session=session,
            user=user,
            base_xp=discovery.xp_reward,
            bonus_percent_override=bonus_percent,
        )
        progress.xp_earned += award.total_xp

        await EventService.track_event(
            session=session,
            user_id=user.id,
            event_type=EventType.DISCOVERY_COMPLETED,
            event_data={
                "discovery_id": str(discovery.id),
                "planet_id": str(planet.id),
                "xp_awarded": award.total_xp,
            },
        )
        await RankService.sync_user_rank(session=session, user=user)
        await cls._commit_and_refresh(session, user, progress)

        return DiscoveryCompletionResult(
            discovery_id=discovery.id,
            planet_id=planet.id,
            completed=True,
            xp_awarded=award.total_xp,
            total_completed_discoveries=len(completed_discovery_ids),
            planet_status=cls._current_planet_status_from_progress(progress, PlanetStatusEnum.IN_PROGRESS),
        )

    @classmethod
    async def complete_practice(
        cls,
        session: AsyncSession,
        *,
        user: User,
        practice: PracticeChallenge,
        submission_result: PracticeSubmissionResult,
        used_solution: bool,
    ) -> PracticeSubmissionResult:
        """Applies practice progression, XP, and artifact side effects."""
        planet = await cls.load_planet_with_content(session=session, planet_id=practice.planet_id)
        planet_status = await cls.ensure_planet_is_unlocked(session=session, user_id=user.id, planet=planet)
        progress = await cls.get_or_create_progress(session=session, user_id=user.id, planet_id=planet.id)

        completed_practice_ids = set(ensure_string_list(progress.completed_practices))
        status = cls.determine_practice_status(
            practice=practice,
            planet=planet,
            completed_practice_ids=completed_practice_ids,
            planet_status=planet_status,
        )
        if status == PracticeStatusEnum.LOCKED:
            raise AppException(message="This practice challenge is locked", status_code=403)

        if not submission_result.passed:
            return submission_result

        if status == PracticeStatusEnum.COMPLETED:
            return submission_result.model_copy(update={"xp_awarded": 0})

        bonus_percent = await XPService.get_total_artifact_bonus_percent(session=session, user_id=user.id)
        completed_practice_ids.add(str(practice.id))
        progress.completed_practices = sorted(completed_practice_ids)
        progress.status = ProgressStatus.IN_PROGRESS.value
        progress.last_activity_at = cls._now()

        base_xp = practice.xp_reward // 2 if used_solution else practice.xp_reward
        award = await XPService.award_user_xp(
            session=session,
            user=user,
            base_xp=base_xp,
            bonus_percent_override=bonus_percent,
        )
        progress.xp_earned += award.total_xp

        await cls._update_planet_completion_if_eligible(
            session=session,
            user=user,
            planet=planet,
            progress=progress,
            bonus_percent_override=bonus_percent,
        )

        await EventService.track_event(
            session=session,
            user_id=user.id,
            event_type=EventType.PRACTICE_COMPLETED,
            event_data={
                "practice_id": str(practice.id),
                "planet_id": str(planet.id),
                "xp_awarded": award.total_xp,
                "used_solution": used_solution,
            },
        )
        await RankService.sync_user_rank(session=session, user=user)
        await cls._commit_and_refresh(session, user, progress)

        return submission_result.model_copy(update={"xp_awarded": award.total_xp})

    @classmethod
    async def submit_quiz(
        cls,
        session: AsyncSession,
        *,
        user: User,
        planet_id: UUID,
        questions: list[QuizQuestion],
        grading_result: QuizSubmitResult,
    ) -> QuizSubmitResult:
        """Persists a quiz attempt and applies its progression consequences."""
        planet = await cls.load_planet_with_content(session=session, planet_id=planet_id)
        planet_status = await cls.ensure_planet_is_unlocked(session=session, user_id=user.id, planet=planet)
        progress = await cls.get_or_create_progress(session=session, user_id=user.id, planet_id=planet.id)

        attempts_result = await session.execute(
            select(QuizAttempt)
            .where(
                QuizAttempt.user_id == user.id,
                QuizAttempt.planet_id == planet.id,
            )
            .order_by(QuizAttempt.attempted_at.desc())
        )
        previous_attempts = attempts_result.scalars().all()
        quiz_status = cls.determine_quiz_status(
            planet=planet,
            progress=progress,
            attempts_count=len(previous_attempts),
            planet_status=planet_status,
        )
        if quiz_status == QuizStatusEnum.LOCKED:
            raise AppException(message="Quiz is locked until all discoveries and practices are completed", status_code=403)

        if progress.quiz_passed and previous_attempts:
            latest_attempt = previous_attempts[0]
            if latest_attempt.attempted_at >= cls._now() - timedelta(hours=24):
                raise AppException(message="Quiz can be retaken 24 hours after a passed attempt", status_code=403)

        bonus_percent = await XPService.get_total_artifact_bonus_percent(session=session, user_id=user.id)
        prior_quiz_xp_awarded = sum(attempt.xp_earned for attempt in previous_attempts)
        pass_base_xp = sum(question.xp_reward for question in questions)
        fail_base_xp = int(round(pass_base_xp * 0.25))
        target_base_xp = pass_base_xp if grading_result.passed else fail_base_xp
        current_target_total = XPService.build_award_result(
            current_xp=0,
            base_xp=target_base_xp,
            bonus_percent=bonus_percent,
        ).total_xp
        xp_to_award = max(current_target_total - prior_quiz_xp_awarded, 0)
        award_total = 0
        if xp_to_award > 0:
            award = await XPService.award_user_xp(
                session=session,
                user=user,
                base_xp=xp_to_award,
                bonus_percent_override=0,
            )
            award_total = award.total_xp
            progress.xp_earned += award.total_xp

        progress.quiz_best_score = max(progress.quiz_best_score or 0, grading_result.score)
        progress.last_activity_at = cls._now()
        artifact_unlocked: ArtifactSummary | None = None

        if grading_result.passed and not progress.quiz_passed:
            progress.quiz_passed = True
            progress.status = ProgressStatus.IN_PROGRESS.value

            completion_artifacts = await cls._update_planet_completion_if_eligible(
                session=session,
                user=user,
                planet=planet,
                progress=progress,
                bonus_percent_override=bonus_percent,
            )
            if completion_artifacts:
                artifact_unlocked = completion_artifacts[0]

            await EventService.track_event(
                session=session,
                user_id=user.id,
                event_type=EventType.QUIZ_PASSED,
                event_data={
                    "planet_id": str(planet.id),
                    "score": grading_result.score,
                    "total_questions": grading_result.total_questions,
                    "xp_awarded": award_total,
                },
            )

        attempt = QuizAttempt(
            user_id=user.id,
            planet_id=planet.id,
            score=grading_result.score,
            total_questions=grading_result.total_questions,
            answers=[result.model_dump(mode="json") for result in grading_result.results],
            passed=grading_result.passed,
            xp_earned=award_total,
            attempted_at=cls._now(),
        )
        session.add(attempt)
        await session.flush()

        await RankService.sync_user_rank(session=session, user=user)
        await cls._commit_and_refresh(session, user, progress, attempt)

        return grading_result.model_copy(
            update={
                "attempt_id": attempt.id,
                "xp_awarded": award_total,
                "quiz_status": QuizStatusEnum.PASSED if grading_result.passed else QuizStatusEnum.FAILED,
                "artifact_unlocked": artifact_unlocked,
            }
        )
