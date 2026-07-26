from __future__ import annotations

from uuid import uuid4

from tests.helpers import (
    assert_error_response,
    assert_success_response,
    create_authenticated_user,
    fetch_planet_by_name,
)


async def test_get_variables_planet_detail(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="planet_variables")
    planet = await fetch_planet_by_name(db_session, "Variables")

    response = await async_client.get(f"/api/v1/planets/{planet.id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["name"] == "Variables"
    assert len(data["discoveries"]) == 5
    assert len(data["practice_challenges"]) == 5
    assert data["quiz"]["total_questions"] == 10
    assert data["artifact"]["name"] == "Variable Vanguard"


async def test_get_data_types_planet_is_locked_for_new_user(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="planet_data_types")
    planet = await fetch_planet_by_name(db_session, "Data Types")

    response = await async_client.get(f"/api/v1/planets/{planet.id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["name"] == "Data Types"
    assert data["status"] == "LOCKED"


async def test_get_planet_returns_not_found_for_unknown_id(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="planet_not_found")

    response = await async_client.get(f"/api/v1/planets/{uuid4()}", headers=user_context["headers"])
    await assert_error_response(response, expected_status=404, expected_message_substring="not found")
