from __future__ import annotations

from tests.helpers import (
    assert_success_response,
    complete_planet,
    create_authenticated_user,
    fetch_planet_by_name,
)


async def test_complete_user_learning_flow(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="complete_flow")

    login_response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": user_context["payload"]["email"],
            "password": user_context["payload"]["password"],
        },
    )
    login_data = await assert_success_response(login_response)
    headers = {"Authorization": f"Bearer {login_data['tokens']['access_token']}"}

    dashboard_response = await async_client.get("/api/v1/dashboard", headers=headers)
    dashboard_data = await assert_success_response(dashboard_response)
    assert dashboard_data["continue_learning"]["planet_name"] == "Variables"

    galaxies_response = await async_client.get("/api/v1/galaxies", headers=headers)
    galaxies = await assert_success_response(galaxies_response)
    assert galaxies[0]["name"] == "Python"

    galaxy_id = galaxies[0]["id"]
    galaxy_detail_response = await async_client.get(f"/api/v1/galaxies/{galaxy_id}", headers=headers)
    galaxy_detail = await assert_success_response(galaxy_detail_response)
    assert len(galaxy_detail["planets"]) == 6
    assert galaxy_detail["planets"][0]["name"] == "Variables"

    variables_planet = await fetch_planet_by_name(db_session, "Variables")
    variables_detail_response = await async_client.get(f"/api/v1/planets/{variables_planet.id}", headers=headers)
    variables_detail = await assert_success_response(variables_detail_response)
    assert variables_detail["quiz"]["total_questions"] == 10

    quiz_result = await complete_planet(async_client, headers, test_session_factory, planet_name="Variables")
    assert quiz_result["passed"] is True
    assert quiz_result["artifact_unlocked"] is not None
    assert quiz_result["artifact_unlocked"]["name"] == "Variable Vanguard"

    artifacts_response = await async_client.get("/api/v1/artifacts", headers=headers)
    artifacts = await assert_success_response(artifacts_response)
    variable_artifact = next(item for item in artifacts if item["artifact"]["name"] == "Variable Vanguard")
    assert variable_artifact["collected"] is True

    data_types_planet = await fetch_planet_by_name(db_session, "Data Types")
    data_types_detail_response = await async_client.get(f"/api/v1/planets/{data_types_planet.id}", headers=headers)
    data_types_detail = await assert_success_response(data_types_detail_response)
    assert data_types_detail["status"] in {"UNLOCKED", "IN_PROGRESS", "COMPLETED"}

    leaderboard_response = await async_client.get(
        "/api/v1/leaderboard?type=global&page=1&limit=20",
        headers=headers,
    )
    leaderboard_data = await assert_success_response(leaderboard_response)
    assert leaderboard_data["user_position"] is not None
    assert leaderboard_data["user_position"]["position"] >= 1
