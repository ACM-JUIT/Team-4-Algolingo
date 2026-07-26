from __future__ import annotations

from tests.helpers import (
    assert_success_response,
    complete_planet,
    create_authenticated_user,
    fetch_artifact_by_name,
    fetch_galaxy_by_name,
)


async def test_artifact_catalog_shows_locked_and_unlocked_states(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="artifact_catalog")

    response = await async_client.get("/api/v1/artifacts", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert len(data) == 6
    variable_artifact = next(item for item in data if item["artifact"]["name"] == "Variable Vanguard")
    assert variable_artifact["collected"] is False


async def test_planet_artifact_is_earned_after_quiz(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="artifact_earned")
    await complete_planet(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    artifact_list_response = await async_client.get("/api/v1/artifacts", headers=user_context["headers"])
    artifact_list = await assert_success_response(artifact_list_response)
    variable_artifact = next(item for item in artifact_list if item["artifact"]["name"] == "Variable Vanguard")
    assert variable_artifact["collected"] is True

    user_artifacts_response = await async_client.get(
        f"/api/v1/users/{user_context['user']['id']}/artifacts",
        headers=user_context["headers"],
    )
    user_artifacts = await assert_success_response(user_artifacts_response)
    assert any(item["artifact"]["name"] == "Variable Vanguard" for item in user_artifacts)


async def test_get_single_artifact_returns_expected_payload(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="artifact_detail")
    artifact = await fetch_artifact_by_name(db_session, "Type Orb")

    response = await async_client.get(f"/api/v1/artifacts/{artifact.id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["name"] == "Type Orb"
    assert data["category"] == "planet"
