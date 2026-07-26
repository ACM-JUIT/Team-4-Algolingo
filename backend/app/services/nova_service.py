from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import httpx
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.models.enums import EventType, NovaSender
from app.models.nova_message import NovaMessage
from app.models.nova_session import NovaSession
from app.models.practice_challenge import PracticeChallenge
from app.models.user import User
from app.schemas.nova import (
    NovaAskRequest,
    NovaContextReference,
    NovaDebugRequest,
    NovaHintRequest,
    NovaMessageRead,
    NovaRecommendRequest,
    NovaResponseData,
)
from app.services.context_builder import ContextBuilder
from app.services.event_service import EventService
from app.services.prompt_builder import PromptBuilder
from app.services.rank_service import RankService

settings = get_settings()
NOVA_MAX_REQUESTS_PER_HOUR = settings.nova_max_requests_per_hour
NOVA_MAX_RESPONSE_TOKENS = settings.nova_max_response_tokens
NOVA_MAX_HISTORY_MESSAGES = settings.nova_max_history_messages
NOVA_TIMEOUT_SECONDS = settings.ollama_timeout_seconds


class NovaService:
    """Coordinates NOVA sessions, persistence, rate limiting, and Ollama calls."""

    @staticmethod
    async def count_recent_requests(session: AsyncSession, *, user_id: UUID) -> int:
        """Counts user-authored NOVA requests within the rolling hourly window."""
        cutoff = datetime.now(UTC).replace(tzinfo=None) - timedelta(hours=1)
        result = await session.execute(
            select(func.count(NovaMessage.id))
            .select_from(NovaMessage)
            .join(NovaSession, NovaSession.id == NovaMessage.session_id)
            .where(
                NovaSession.user_id == user_id,
                NovaMessage.sender == NovaSender.USER.value,
                NovaMessage.created_at >= cutoff,
            )
        )
        return int(result.scalar_one() or 0)

    @classmethod
    async def ensure_within_rate_limit(cls, session: AsyncSession, *, user_id: UUID) -> None:
        recent_request_count = await cls.count_recent_requests(session=session, user_id=user_id)
        if recent_request_count >= NOVA_MAX_REQUESTS_PER_HOUR:
            raise AppException(message="NOVA request limit reached. Try again later.", status_code=429)

    @staticmethod
    async def get_session(
        session: AsyncSession,
        *,
        user_id: UUID,
        session_id: UUID,
    ) -> NovaSession:
        result = await session.execute(
            select(NovaSession)
            .options(selectinload(NovaSession.messages))
            .where(
                NovaSession.id == session_id,
                NovaSession.user_id == user_id,
            )
        )
        nova_session = result.scalar_one_or_none()
        if nova_session is None:
            raise AppException(message="NOVA session not found", status_code=404)
        return nova_session

    @classmethod
    async def get_or_create_session(
        cls,
        session: AsyncSession,
        *,
        user: User,
        session_id: UUID | None,
        title_seed: str,
    ) -> NovaSession:
        if session_id is not None:
            return await cls.get_session(session=session, user_id=user.id, session_id=session_id)

        nova_session = NovaSession(
            user_id=user.id,
            title=PromptBuilder.build_session_title(title_seed),
        )
        session.add(nova_session)
        await session.flush()
        return nova_session

    @staticmethod
    async def get_recent_session_messages(
        session: AsyncSession,
        *,
        session_id: UUID,
        limit: int = NOVA_MAX_HISTORY_MESSAGES,
    ) -> list[NovaMessage]:
        result = await session.execute(
            select(NovaMessage)
            .where(NovaMessage.session_id == session_id)
            .order_by(NovaMessage.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return list(reversed(messages))

    @staticmethod
    async def store_message(
        session: AsyncSession,
        *,
        session_id: UUID,
        sender: NovaSender,
        message: str,
        context_data: dict[str, Any] | None,
    ) -> NovaMessage:
        nova_message = NovaMessage(
            session_id=session_id,
            sender=sender.value,
            message=message,
            context_data=context_data,
        )
        session.add(nova_message)
        await session.flush()
        return nova_message

    @staticmethod
    def serialize_messages(messages: list[NovaMessage]) -> list[NovaMessageRead]:
        return [NovaMessageRead.model_validate(message) for message in messages]

    @staticmethod
    async def call_ollama(*, messages: list[dict[str, str]]) -> str:
        url = f"{str(settings.ollama_base_url).rstrip('/')}/api/chat"
        payload = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": NOVA_MAX_RESPONSE_TOKENS,
                "temperature": 0.3,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=NOVA_TIMEOUT_SECONDS) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise AppException(message="NOVA request timed out", status_code=504) from exc
        except httpx.HTTPError as exc:
            raise AppException(message="NOVA service is currently unavailable", status_code=502) from exc

        message_data = data.get("message") or {}
        content = message_data.get("content") or data.get("response")
        if not content:
            raise AppException(message="NOVA returned an empty response", status_code=502)
        return str(content).strip()

    @classmethod
    async def _finalize_interaction(
        cls,
        session: AsyncSession,
        *,
        user: User,
        nova_session: NovaSession,
        reply: str,
        context_data: dict[str, Any],
        mode: str,
    ) -> NovaResponseData:
        await cls.store_message(
            session=session,
            session_id=nova_session.id,
            sender=NovaSender.ASSISTANT,
            message=reply,
            context_data=context_data,
        )

        await EventService.track_event(
            session=session,
            user_id=user.id,
            event_type=EventType.NOVA_USED,
            event_data={
                "mode": mode,
                "session_id": str(nova_session.id),
            },
        )
        await RankService.sync_user_rank(session=session, user=user)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise

        final_messages = await cls.get_recent_session_messages(session=session, session_id=nova_session.id)
        return NovaResponseData(
            session_id=nova_session.id,
            reply=reply,
            messages=cls.serialize_messages(final_messages),
        )

    @classmethod
    async def _run_interaction(
        cls,
        session: AsyncSession,
        *,
        user: User,
        session_id: UUID | None,
        user_message: str,
        reference: NovaContextReference,
        mode: str,
    ) -> NovaResponseData:
        await cls.ensure_within_rate_limit(session=session, user_id=user.id)

        nova_session = await cls.get_or_create_session(
            session=session,
            user=user,
            session_id=session_id,
            title_seed=user_message or mode,
        )
        recent_messages = await cls.get_recent_session_messages(session=session, session_id=nova_session.id)
        context_data = await ContextBuilder.build_context(
            session=session,
            user=user,
            reference=reference,
            session_messages=recent_messages,
        )

        await cls.store_message(
            session=session,
            session_id=nova_session.id,
            sender=NovaSender.USER,
            message=user_message,
            context_data=context_data,
        )

        prompt_messages = [
            {
                "role": "system",
                "content": PromptBuilder.build_system_prompt(mode=mode, context=context_data),
            },
            *ContextBuilder.serialize_history(recent_messages),
            {
                "role": "user",
                "content": PromptBuilder.build_user_message(mode=mode, raw_message=user_message, context=context_data),
            },
        ]
        reply = await cls.call_ollama(messages=prompt_messages)
        return await cls._finalize_interaction(
            session=session,
            user=user,
            nova_session=nova_session,
            reply=reply,
            context_data=context_data,
            mode=mode,
        )

    @classmethod
    async def ask(cls, session: AsyncSession, *, user: User, payload: NovaAskRequest) -> NovaResponseData:
        """Handles a general NOVA question."""
        return await cls._run_interaction(
            session=session,
            user=user,
            session_id=payload.session_id,
            user_message=payload.message,
            reference=NovaContextReference(
                galaxy_id=payload.galaxy_id,
                planet_id=payload.planet_id,
                discovery_id=payload.discovery_id,
                practice_id=payload.practice_id,
            ),
            mode="ask",
        )

    @classmethod
    async def hint(
        cls,
        session: AsyncSession,
        *,
        user: User,
        practice_id: UUID,
        payload: NovaHintRequest,
    ) -> NovaResponseData:
        """Generates a guided NOVA hint for a practice challenge."""
        practice = await session.get(PracticeChallenge, practice_id)
        if practice is None:
            raise AppException(message="Practice challenge not found", status_code=404)

        request_message = (
            f"Practice: {practice.title}. "
            f"Specific problem: {payload.specific_problem or 'Need a helpful hint.'}. "
            f"Current code: {payload.current_code or 'No code provided.'}"
        )
        return await cls._run_interaction(
            session=session,
            user=user,
            session_id=payload.session_id,
            user_message=request_message,
            reference=NovaContextReference(planet_id=practice.planet_id, practice_id=practice.id),
            mode="hint",
        )

    @classmethod
    async def debug(cls, session: AsyncSession, *, user: User, payload: NovaDebugRequest) -> NovaResponseData:
        """Requests NOVA debugging assistance for a code sample."""
        request_message = (
            f"Problem description: {payload.problem_description or 'Debug this code.'}\n\n"
            f"Code:\n```python\n{payload.code}\n```"
        )
        return await cls._run_interaction(
            session=session,
            user=user,
            session_id=payload.session_id,
            user_message=request_message,
            reference=NovaContextReference(
                galaxy_id=payload.galaxy_id,
                planet_id=payload.planet_id,
                practice_id=payload.practice_id,
            ),
            mode="debug",
        )

    @classmethod
    async def recommend(cls, session: AsyncSession, *, user: User, payload: NovaRecommendRequest) -> NovaResponseData:
        """Requests a NOVA recommendation for the next learning step."""
        request_message = "Recommend the best next topic or review step based on my current progress."
        return await cls._run_interaction(
            session=session,
            user=user,
            session_id=payload.session_id,
            user_message=request_message,
            reference=NovaContextReference(
                galaxy_id=payload.galaxy_id,
                planet_id=payload.planet_id,
            ),
            mode="recommend",
        )
