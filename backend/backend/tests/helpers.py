from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID, uuid4

from httpx import AsyncClient, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.artifact import Artifact
from app.models.discovery import Discovery
from app.models.galaxy import Galaxy
from app.models.nova_message import NovaMessage
from app.models.nova_session import NovaSession
from app.models.planet import Planet
from app.models.practice_challenge import PracticeChallenge
from app.models.quiz_question import QuizQuestion
from app.models.user import User
from app.models.user_artifact import UserArtifact
from app.models.user_progress import UserProgress


def build_user_payload(prefix: str = "integration") -> dict[str, str]:
    unique_suffix = uuid4().hex[:8]
    username = f"{prefix}_{unique_suffix}"
    email = f"{username}@example.com"
    password = "StrongPass1"
    return {
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password,
    }


def build_auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


async def assert_success_response(response: Response, expected_status: int = 200) -> dict:
    assert response.status_code == expected_status, response.text
    payload = response.json()
    assert payload["success"] is True, payload
    assert "data" in payload, payload
    return payload["data"]


async def assert_error_response(
    response: Response,
    *,
    expected_status: int,
    expected_message_substring: str | None = None,
) -> dict:
    assert response.status_code == expected_status, response.text
    payload = response.json()
    assert payload["success"] is False, payload
    if expected_message_substring is not None:
        assert expected_message_substring.lower() in payload["message"].lower(), payload
    return payload


async def create_authenticated_user(async_client: AsyncClient, prefix: str = "integration") -> dict[str, object]:
    payload = build_user_payload(prefix)
    register_response = await async_client.post("/api/v1/auth/register", json=payload)
    register_data = await assert_success_response(register_response, expected_status=201)
    return {
        "payload": payload,
        "user": register_data["user"],
        "tokens": register_data["tokens"],
        "headers": build_auth_headers(register_data["tokens"]["access_token"]),
    }


async def login_user(async_client: AsyncClient, *, email: str, password: str) -> dict:
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    return await assert_success_response(response)


async def fetch_galaxy_by_name(session: AsyncSession, name: str) -> Galaxy:
    result = await session.execute(select(Galaxy).where(Galaxy.name == name))
    galaxy = result.scalar_one_or_none()
    assert galaxy is not None, f"Galaxy '{name}' was not found in the test database."
    return galaxy


async def fetch_planet_by_name(session: AsyncSession, name: str) -> Planet:
    result = await session.execute(select(Planet).where(Planet.name == name))
    planet = result.scalar_one_or_none()
    assert planet is not None, f"Planet '{name}' was not found in the test database."
    return planet


async def fetch_discoveries_for_planet(session: AsyncSession, planet_id: UUID) -> list[Discovery]:
    result = await session.execute(
        select(Discovery)
        .where(Discovery.planet_id == planet_id)
        .order_by(Discovery.order_number.asc())
    )
    return list(result.scalars().all())


async def fetch_practices_for_planet(session: AsyncSession, planet_id: UUID) -> list[PracticeChallenge]:
    result = await session.execute(
        select(PracticeChallenge)
        .where(PracticeChallenge.planet_id == planet_id)
        .order_by(PracticeChallenge.order_number.asc())
    )
    return list(result.scalars().all())


async def fetch_quiz_questions_for_planet(session: AsyncSession, planet_id: UUID) -> list[QuizQuestion]:
    result = await session.execute(
        select(QuizQuestion)
        .where(QuizQuestion.planet_id == planet_id)
        .order_by(QuizQuestion.order_number.asc())
    )
    return list(result.scalars().all())


async def fetch_user_progress(
    session: AsyncSession,
    *,
    user_id: UUID,
    planet_id: UUID,
) -> UserProgress | None:
    result = await session.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.planet_id == planet_id,
        )
    )
    return result.scalar_one_or_none()


async def fetch_user_artifact(
    session: AsyncSession,
    *,
    user_id: UUID,
    artifact_id: UUID,
) -> UserArtifact | None:
    result = await session.execute(
        select(UserArtifact).where(
            UserArtifact.user_id == user_id,
            UserArtifact.artifact_id == artifact_id,
        )
    )
    return result.scalar_one_or_none()


async def fetch_artifact_by_name(session: AsyncSession, name: str) -> Artifact:
    result = await session.execute(select(Artifact).where(Artifact.name == name))
    artifact = result.scalar_one_or_none()
    assert artifact is not None, f"Artifact '{name}' was not found in the test database."
    return artifact


async def fetch_nova_session_for_user(session: AsyncSession, user_id: UUID) -> NovaSession | None:
    result = await session.execute(select(NovaSession).where(NovaSession.user_id == user_id))
    return result.scalar_one_or_none()


async def fetch_nova_messages_for_session(session: AsyncSession, session_id: UUID) -> list[NovaMessage]:
    result = await session.execute(
        select(NovaMessage)
        .where(NovaMessage.session_id == session_id)
        .order_by(NovaMessage.created_at.asc())
    )
    return list(result.scalars().all())


def build_correct_quiz_answers(questions: Sequence[QuizQuestion]) -> list[dict[str, str]]:
    return [
        {
            "question_id": str(question.id),
            "answer": question.correct_answer,
        }
        for question in questions
    ]


async def complete_discoveries(
    async_client: AsyncClient,
    headers: dict[str, str],
    session_factory: async_sessionmaker[AsyncSession],
    *,
    planet_name: str,
) -> None:
    async with session_factory() as session:
        planet = await fetch_planet_by_name(session, planet_name)
        discoveries = await fetch_discoveries_for_planet(session, planet.id)

    for discovery in discoveries:
        response = await async_client.post(
            f"/api/v1/discoveries/{discovery.id}/complete",
            headers=headers,
        )
        assert response.status_code == 200, response.text


async def complete_practices(
    async_client: AsyncClient,
    headers: dict[str, str],
    session_factory: async_sessionmaker[AsyncSession],
    *,
    planet_name: str,
) -> None:
    async with session_factory() as session:
        planet = await fetch_planet_by_name(session, planet_name)
        practices = await fetch_practices_for_planet(session, planet.id)

    for practice in practices:
        assert practice.solution_code is not None, f"Practice '{practice.title}' has no solution_code."
        response = await async_client.post(
            f"/api/v1/practices/{practice.id}/submit",
            headers=headers,
            json={"submitted_code": practice.solution_code},
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["data"]["passed"] is True, payload


async def complete_planet(
    async_client: AsyncClient,
    headers: dict[str, str],
    session_factory: async_sessionmaker[AsyncSession],
    *,
    planet_name: str,
) -> dict:
    await complete_discoveries(async_client, headers, session_factory, planet_name=planet_name)
    await complete_practices(async_client, headers, session_factory, planet_name=planet_name)

    async with session_factory() as session:
        planet = await fetch_planet_by_name(session, planet_name)
        questions = await fetch_quiz_questions_for_planet(session, planet.id)

    response = await async_client.post(
        f"/api/v1/planets/{planet.id}/quiz/submit",
        headers=headers,
        json={"answers": build_correct_quiz_answers(questions)},
    )
    return await assert_success_response(response)
