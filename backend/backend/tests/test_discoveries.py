from __future__ import annotations

from uuid import uuid4

from tests.helpers import (
    assert_error_response,
    assert_success_response,
    create_authenticated_user,
    fetch_discoveries_for_planet,
    fetch_planet_by_name,
    fetch_user_progress,
)


async def test_get_discovery_returns_markdown_content(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="discovery_get")
    planet = await fetch_planet_by_name(db_session, "Variables")
    discoveries = await fetch_discoveries_for_planet(db_session, planet.id)

    response = await async_client.get(f"/api/v1/discoveries/{discoveries[0].id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["title"] == discoveries[0].title
    assert data["content_md"]


async def test_complete_first_discovery_updates_progress(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="discovery_complete")
    user_id = user_context["user"]["id"]
    planet = await fetch_planet_by_name(db_session, "Variables")
    discoveries = await fetch_discoveries_for_planet(db_session, planet.id)

    response = await async_client.post(
        f"/api/v1/discoveries/{discoveries[0].id}/complete",
        headers=user_context["headers"],
    )
    data = await assert_success_response(response)

    assert data["xp_awarded"] > 0
    async with test_session_factory() as session:
        progress = await fetch_user_progress(session, user_id=user_id, planet_id=planet.id)
        assert progress is not None
        assert str(discoveries[0].id) in progress.completed_discoveries


async def test_discovery_sequence_is_enforced(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="discovery_lock")
    planet = await fetch_planet_by_name(db_session, "Variables")
    discoveries = await fetch_discoveries_for_planet(db_session, planet.id)

    response = await async_client.post(
        f"/api/v1/discoveries/{discoveries[1].id}/complete",
        headers=user_context["headers"],
    )
    await assert_error_response(response, expected_status=403, expected_message_substring="locked")


async def test_duplicate_discovery_completion_does_not_duplicate_xp(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="discovery_duplicate")
    planet = await fetch_planet_by_name(db_session, "Variables")
    discoveries = await fetch_discoveries_for_planet(db_session, planet.id)

    first = await async_client.post(
        f"/api/v1/discoveries/{discoveries[0].id}/complete",
        headers=user_context["headers"],
    )
    await assert_success_response(first)

    second = await async_client.post(
        f"/api/v1/discoveries/{discoveries[0].id}/complete",
        headers=user_context["headers"],
    )
    data = await assert_success_response(second)

    assert data["xp_awarded"] == 0


async def test_unknown_discovery_returns_not_found(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="discovery_missing")
    response = await async_client.get(f"/api/v1/discoveries/{uuid4()}", headers=user_context["headers"])
    await assert_error_response(response, expected_status=404, expected_message_substring="not found")
