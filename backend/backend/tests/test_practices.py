from __future__ import annotations

from uuid import uuid4

from tests.helpers import (
    assert_error_response,
    assert_success_response,
    create_authenticated_user,
    fetch_planet_by_name,
    fetch_practices_for_planet,
)


async def test_get_practice_returns_details(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="practice_get")
    planet = await fetch_planet_by_name(db_session, "Variables")
    practices = await fetch_practices_for_planet(db_session, planet.id)

    response = await async_client.get(f"/api/v1/practices/{practices[0].id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["title"] == practices[0].title
    assert data["challenge_type"] == practices[0].challenge_type


async def test_submit_correct_practice_solution(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="practice_correct")
    planet = await fetch_planet_by_name(db_session, "Variables")
    practice = (await fetch_practices_for_planet(db_session, planet.id))[0]
    assert practice.solution_code is not None

    response = await async_client.post(
        f"/api/v1/practices/{practice.id}/submit",
        headers=user_context["headers"],
        json={"submitted_code": practice.solution_code},
    )
    data = await assert_success_response(response)

    assert data["passed"] is True
    assert data["xp_awarded"] > 0


async def test_submit_incorrect_practice_solution(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="practice_incorrect")
    planet = await fetch_planet_by_name(db_session, "Variables")
    practice = (await fetch_practices_for_planet(db_session, planet.id))[0]

    response = await async_client.post(
        f"/api/v1/practices/{practice.id}/submit",
        headers=user_context["headers"],
        json={"submitted_code": 'print("Wrong answer")'},
    )
    data = await assert_success_response(response)

    assert data["passed"] is False
    assert data["xp_awarded"] == 0


async def test_submit_practice_with_syntax_error(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="practice_syntax")
    planet = await fetch_planet_by_name(db_session, "Variables")
    practice = (await fetch_practices_for_planet(db_session, planet.id))[0]

    response = await async_client.post(
        f"/api/v1/practices/{practice.id}/submit",
        headers=user_context["headers"],
        json={"submitted_code": "def broken("},
    )

    await assert_error_response(response, expected_status=400, expected_message_substring="syntax error")


async def test_duplicate_practice_submission_does_not_duplicate_xp(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="practice_duplicate")
    planet = await fetch_planet_by_name(db_session, "Variables")
    practice = (await fetch_practices_for_planet(db_session, planet.id))[0]
    assert practice.solution_code is not None

    first = await async_client.post(
        f"/api/v1/practices/{practice.id}/submit",
        headers=user_context["headers"],
        json={"submitted_code": practice.solution_code},
    )
    first_data = await assert_success_response(first)
    assert first_data["passed"] is True

    second = await async_client.post(
        f"/api/v1/practices/{practice.id}/submit",
        headers=user_context["headers"],
        json={"submitted_code": practice.solution_code},
    )
    second_data = await assert_success_response(second)

    assert second_data["passed"] is True
    assert second_data["xp_awarded"] == 0


async def test_unknown_practice_returns_not_found(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="practice_missing")
    response = await async_client.get(f"/api/v1/practices/{uuid4()}", headers=user_context["headers"])
    await assert_error_response(response, expected_status=404, expected_message_substring="not found")
