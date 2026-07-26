from __future__ import annotations

from tests.helpers import (
    assert_success_response,
    create_authenticated_user,
    fetch_discoveries_for_planet,
    fetch_galaxy_by_name,
    fetch_planet_by_name,
)


async def test_global_leaderboard_returns_current_user_position(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="leaderboard_global")

    response = await async_client.get(
        "/api/v1/leaderboard?type=global&page=1&limit=20",
        headers=user_context["headers"],
    )
    data = await assert_success_response(response)

    assert data["leaderboard_type"] == "global"
    assert data["page"] == 1
    assert data["limit"] == 20
    assert data["user_position"] is not None
    assert data["user_position"]["position"] >= 1


async def test_galaxy_leaderboard_returns_user_position_after_progress(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="leaderboard_galaxy")
    planet = await fetch_planet_by_name(db_session, "Variables")
    discovery = (await fetch_discoveries_for_planet(db_session, planet.id))[0]
    await async_client.post(
        f"/api/v1/discoveries/{discovery.id}/complete",
        headers=user_context["headers"],
    )
    galaxy = await fetch_galaxy_by_name(db_session, "Python")

    response = await async_client.get(
        f"/api/v1/leaderboard?type=galaxy&galaxy_id={galaxy.id}",
        headers=user_context["headers"],
    )
    data = await assert_success_response(response)

    assert data["leaderboard_type"] == "galaxy"
    assert data["user_position"] is not None
    assert data["user_position"]["position"] >= 1
