from __future__ import annotations

from tests.helpers import (
    assert_error_response,
    assert_success_response,
    build_auth_headers,
    build_user_payload,
    create_authenticated_user,
)


async def test_register_creates_user_and_tokens(async_client) -> None:
    payload = build_user_payload("auth_register")

    response = await async_client.post("/api/v1/auth/register", json=payload)
    data = await assert_success_response(response, expected_status=201)

    assert data["user"]["username"] == payload["username"]
    assert data["user"]["email"] == payload["email"]
    assert data["tokens"]["access_token"]
    assert data["tokens"]["refresh_token"]
    assert data["tokens"]["token_type"] == "bearer"


async def test_register_rejects_duplicate_email(async_client) -> None:
    payload = build_user_payload("auth_duplicate")

    first_response = await async_client.post("/api/v1/auth/register", json=payload)
    await assert_success_response(first_response, expected_status=201)

    duplicate_response = await async_client.post("/api/v1/auth/register", json=payload)
    await assert_error_response(duplicate_response, expected_status=409, expected_message_substring="already")


async def test_login_returns_new_token_pair(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="auth_login")

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": user_context["payload"]["email"],
            "password": user_context["payload"]["password"],
        },
    )
    data = await assert_success_response(response)

    assert data["user"]["email"] == user_context["payload"]["email"]
    assert data["tokens"]["access_token"]
    assert data["tokens"]["refresh_token"]


async def test_login_rejects_invalid_password(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="auth_wrong_password")

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": user_context["payload"]["email"],
            "password": "WrongPass1",
        },
    )

    await assert_error_response(response, expected_status=401, expected_message_substring="invalid")


async def test_auth_me_returns_current_user(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="auth_me")

    response = await async_client.get("/api/v1/auth/me", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert data["user"]["id"] == user_context["user"]["id"]
    assert data["user"]["username"] == user_context["payload"]["username"]


async def test_refresh_rotates_tokens(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="auth_refresh")
    old_refresh_token = user_context["tokens"]["refresh_token"]

    response = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    data = await assert_success_response(response)

    assert data["tokens"]["access_token"]
    assert data["tokens"]["refresh_token"]
    assert data["tokens"]["refresh_token"] != old_refresh_token


async def test_logout_revokes_refresh_token(async_client) -> None:
    user_context = await create_authenticated_user(async_client, prefix="auth_logout")
    refresh_token = user_context["tokens"]["refresh_token"]

    logout_response = await async_client.post(
        "/api/v1/auth/logout",
        headers=user_context["headers"],
        json={"refresh_token": refresh_token},
    )
    logout_data = await assert_success_response(logout_response)
    assert logout_data["logged_out"] is True

    refresh_response = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    await assert_error_response(refresh_response, expected_status=401)


async def test_protected_auth_route_requires_authentication(async_client) -> None:
    response = await async_client.get("/api/v1/auth/me")
    await assert_error_response(response, expected_status=401, expected_message_substring="not authenticated")


async def test_auth_me_rejects_malformed_access_token(async_client) -> None:
    response = await async_client.get(
        "/api/v1/auth/me",
        headers=build_auth_headers("not-a-jwt-token"),
    )
    await assert_error_response(response, expected_status=401)
