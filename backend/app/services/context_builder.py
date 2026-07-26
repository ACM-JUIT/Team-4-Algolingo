from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.discovery import Discovery
from app.models.enums import NovaSender
from app.models.galaxy import Galaxy
from app.models.nova_message import NovaMessage
from app.models.planet import Planet
from app.models.practice_challenge import PracticeChallenge
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User
from app.models.user_progress import UserProgress
from app.schemas.event import UserEventRead
from app.schemas.nova import NovaContextReference
from app.services.event_service import EventService
from app.services.service_utils import ensure_string_list

VALID_HISTORY_ROLES = {NovaSender.USER.value, NovaSender.ASSISTANT.value, NovaSender.SYSTEM.value}
RECENT_QUIZ_LIMIT = 3
RECENT_ACTIVITY_LIMIT = 5


class ContextBuilder:
    """Builds sanitized NOVA context from user state and learning progress."""

    @staticmethod
    def serialize_history(messages: list[NovaMessage]) -> list[dict[str, str]]:
        """Serializes stored NOVA messages into chat-history payloads."""
        history: list[dict[str, str]] = []
        for message in messages:
            if not message.message:
                continue
            role = message.sender if message.sender in VALID_HISTORY_ROLES else NovaSender.USER.value
            history.append({"role": role, "content": message.message})
        return history

    @staticmethod
    def summarize_recent_activity(events: list[UserEventRead]) -> list[str]:
        """Returns recent activity names for NOVA prompts."""
        return [str(event.event_type) for event in events]

    @staticmethod
    def summarize_quiz_performance(attempts: list[QuizAttempt]) -> list[dict[str, Any]]:
        """Builds recent quiz performance snippets for prompt context."""
        return [
            {
                "planet_id": str(attempt.planet_id),
                "score": attempt.score,
                "total_questions": attempt.total_questions,
                "passed": attempt.passed,
                "attempted_at": attempt.attempted_at.isoformat(),
            }
            for attempt in attempts
        ]

    @staticmethod
    def summarize_progress(progress: UserProgress | None) -> dict[str, Any]:
        """Builds a compact progress summary for NOVA."""
        if progress is None:
            return {
                "completed_discoveries": [],
                "completed_practices": [],
                "quiz_passed": False,
                "quiz_best_score": None,
                "completed": False,
                "status": None,
                "xp_earned": 0,
            }
        return {
            "completed_discoveries": ensure_string_list(progress.completed_discoveries),
            "completed_practices": ensure_string_list(progress.completed_practices),
            "quiz_passed": progress.quiz_passed,
            "quiz_best_score": progress.quiz_best_score,
            "completed": progress.completed,
            "status": progress.status,
            "xp_earned": progress.xp_earned,
        }

    @classmethod
    async def build_context(
        cls,
        session: AsyncSession,
        *,
        user: User,
        reference: NovaContextReference,
        session_messages: list[NovaMessage],
    ) -> dict[str, Any]:
        """Builds the sanitized, session-aware NOVA prompt context."""
        context: dict[str, Any] = {
            "user_id": str(user.id),
            "user_level": user.level,
            "user_rank": user.rank_title,
            "user_xp": user.xp,
            "streak_days": user.streak_days,
            "current_galaxy": None,
            "current_planet": None,
            "current_discovery": None,
            "current_practice": None,
            "current_topic": None,
            "user_progress": {},
            "recent_quiz_performance": [],
            "recent_activity": [],
            "conversation_history": cls.serialize_history(session_messages),
        }

        galaxy: Galaxy | None = None
        planet: Planet | None = None

        if reference.discovery_id is not None:
            result = await session.execute(
                select(Discovery)
                .options(selectinload(Discovery.planet).selectinload(Planet.galaxy))
                .where(Discovery.id == reference.discovery_id)
            )
            discovery = result.scalar_one_or_none()
            if discovery is not None:
                planet = discovery.planet
                galaxy = planet.galaxy
                context["current_discovery"] = {
                    "id": str(discovery.id),
                    "title": discovery.title,
                    "learning_objective": discovery.learning_objective,
                }
                context["current_topic"] = discovery.title

        if reference.practice_id is not None:
            result = await session.execute(
                select(PracticeChallenge)
                .options(selectinload(PracticeChallenge.planet).selectinload(Planet.galaxy))
                .where(PracticeChallenge.id == reference.practice_id)
            )
            practice = result.scalar_one_or_none()
            if practice is not None:
                planet = practice.planet
                galaxy = planet.galaxy
                context["current_practice"] = {
                    "id": str(practice.id),
                    "title": practice.title,
                    "challenge_type": practice.challenge_type,
                    "learning_outcome": practice.learning_outcome,
                }
                context["current_topic"] = practice.title

        if reference.planet_id is not None and planet is None:
            result = await session.execute(
                select(Planet)
                .options(selectinload(Planet.galaxy))
                .where(Planet.id == reference.planet_id)
            )
            planet = result.scalar_one_or_none()
            if planet is not None:
                galaxy = planet.galaxy
                context["current_topic"] = planet.name

        if reference.galaxy_id is not None and galaxy is None:
            galaxy = await session.get(Galaxy, reference.galaxy_id)

        if galaxy is not None:
            context["current_galaxy"] = {
                "id": str(galaxy.id),
                "name": galaxy.name,
                "programming_language": galaxy.programming_language,
            }
        if planet is not None:
            context["current_planet"] = {
                "id": str(planet.id),
                "name": planet.name,
                "tagline": planet.tagline,
                "difficulty": planet.difficulty,
            }
            if context["current_topic"] is None:
                context["current_topic"] = planet.name

            progress_result = await session.execute(
                select(UserProgress).where(
                    UserProgress.user_id == user.id,
                    UserProgress.planet_id == planet.id,
                )
            )
            progress = progress_result.scalar_one_or_none()
            context["user_progress"] = cls.summarize_progress(progress)

            quiz_result = await session.execute(
                select(QuizAttempt)
                .where(
                    QuizAttempt.user_id == user.id,
                    QuizAttempt.planet_id == planet.id,
                )
                .order_by(QuizAttempt.attempted_at.desc())
                .limit(RECENT_QUIZ_LIMIT)
            )
            context["recent_quiz_performance"] = cls.summarize_quiz_performance(quiz_result.scalars().all())

        recent_activity = await EventService.list_recent_events(session=session, user_id=user.id, limit=RECENT_ACTIVITY_LIMIT)
        context["recent_activity"] = cls.summarize_recent_activity(recent_activity)
        return context
