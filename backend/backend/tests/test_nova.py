from __future__ import annotations

from tests.helpers import (
    assert_success_response,
    create_authenticated_user,
    fetch_nova_messages_for_session,
    fetch_nova_session_for_user,
    fetch_planet_by_name,
    fetch_practices_for_planet,
)
from app.services.nova_service import NovaService


async def test_nova_ask_persists_session_and_messages(async_client, db_session, monkeypatch) -> None:
    user_context = await create_authenticated_user(async_client, prefix="nova_ask")

    async def fake_call_ollama(*, messages):
        assert messages
        return "Captain, variables store values."

    monkeypatch.setattr(NovaService, "call_ollama", fake_call_ollama)

    response = await async_client.post(
        "/api/v1/nova/ask",
        headers=user_context["headers"],
        json={
            "message": "Explain variables",
            "session_id": None,
            "galaxy_id": None,
            "planet_id": None,
            "discovery_id": None,
            "practice_id": None,
        },
    )
    data = await assert_success_response(response)

    assert data["reply"] == "Captain, variables store values."

    nova_session = await fetch_nova_session_for_user(db_session, user_context["user"]["id"])
    assert nova_session is not None
    messages = await fetch_nova_messages_for_session(db_session, nova_session.id)
    assert len(messages) >= 2


async def test_nova_hint_endpoint(async_client, db_session, monkeypatch) -> None:
    user_context = await create_authenticated_user(async_client, prefix="nova_hint")
    planet = await fetch_planet_by_name(db_session, "Variables")
    practice = (await fetch_practices_for_planet(db_session, planet.id))[0]

    async def fake_call_ollama(*, messages):
        return "Try using print first."

    monkeypatch.setattr(NovaService, "call_ollama", fake_call_ollama)

    response = await async_client.post(
        f"/api/v1/nova/hint/{practice.id}",
        headers=user_context["headers"],
        json={"current_code": "", "specific_problem": "Need help", "session_id": None},
    )
    data = await assert_success_response(response)
    assert "print" in data["reply"].lower()


async def test_nova_debug_endpoint(async_client, monkeypatch) -> None:
    user_context = await create_authenticated_user(async_client, prefix="nova_debug")

    async def fake_call_ollama(*, messages):
        return "You missed a colon."

    monkeypatch.setattr(NovaService, "call_ollama", fake_call_ollama)

    response = await async_client.post(
        "/api/v1/nova/debug",
        headers=user_context["headers"],
        json={
            "code": "if True print('x')",
            "problem_description": "syntax error",
            "session_id": None,
            "galaxy_id": None,
            "planet_id": None,
            "practice_id": None,
        },
    )
    data = await assert_success_response(response)
    assert "colon" in data["reply"].lower()


async def test_nova_recommend_endpoint(async_client, monkeypatch) -> None:
    user_context = await create_authenticated_user(async_client, prefix="nova_recommend")

    async def fake_call_ollama(*, messages):
        return "Review Data Types next."

    monkeypatch.setattr(NovaService, "call_ollama", fake_call_ollama)

    response = await async_client.post(
        "/api/v1/nova/recommend",
        headers=user_context["headers"],
        json={"session_id": None, "galaxy_id": None, "planet_id": None},
    )
    data = await assert_success_response(response)
    assert "data types" in data["reply"].lower()
