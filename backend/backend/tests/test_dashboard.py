from __future__ import annotations

from tests.helpers import assert_success_response, create_authenticated_user


async def test_dashboard_returns_expected_structure_for_new_user(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="dashboard")

    response = await async_client.get("/api/v1/dashboard", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["user"]["username"] == user_context["payload"]["username"]
    assert data["quick_stats"]["xp"] >= 0
    assert data["quick_stats"]["level"] >= 1
    assert data["continue_learning"] is not None
    assert data["continue_learning"]["planet_name"] == "Variables"
    assert isinstance(data["recent_activity"], list)
