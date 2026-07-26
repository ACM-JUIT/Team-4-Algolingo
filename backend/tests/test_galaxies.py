from __future__ import annotations

from tests.helpers import assert_success_response, create_authenticated_user, fetch_galaxy_by_name


async def test_list_galaxies_returns_python_galaxy(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="galaxy_list")

    response = await async_client.get("/api/v1/galaxies", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert len(data) == 1
    assert data[0]["name"] == "Python"
    assert data[0]["programming_language"] == "Python"


async def test_get_python_galaxy_detail_returns_six_planets(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="galaxy_detail")
    galaxy = await fetch_galaxy_by_name(db_session, "Python")

    response = await async_client.get(f"/api/v1/galaxies/{galaxy.id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["name"] == "Python"
    assert len(data["planets"]) == 6
    assert data["planets"][0]["name"] == "Variables"
    assert data["planets"][1]["name"] == "Data Types"
    assert data["planets"][0]["status"] == "UNLOCKED"
    assert data["planets"][1]["status"] == "LOCKED"
