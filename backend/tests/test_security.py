from __future__ import annotations

from app.core.security import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)


def test_password_hash_and_verify() -> None:
    password = "StrongPass1"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password) is True
    assert verify_password("WrongPass1", hashed_password) is False


def test_access_token_generation_and_decode() -> None:
    token, _ = create_access_token(subject="user-1", username="captain", role="USER")
    payload = decode_token(token)

    assert payload["sub"] == "user-1"
    assert payload["username"] == "captain"
    assert payload["role"] == "USER"
    assert payload["type"] == ACCESS_TOKEN_TYPE


def test_decode_token_tolerates_surrounding_quotes_and_whitespace() -> None:
    token, _ = create_access_token(subject="user-1", username="captain", role="USER")
    payload = decode_token(f'  "{token}"  ')

    assert payload["sub"] == "user-1"
    assert payload["username"] == "captain"


def test_refresh_token_generation_and_decode() -> None:
    token, _, jti = create_refresh_token(subject="user-1", username="captain", role="USER")
    payload = decode_token(token)

    assert payload["sub"] == "user-1"
    assert payload["type"] == REFRESH_TOKEN_TYPE
    assert payload["jti"] == jti


def test_hash_token_is_deterministic() -> None:
    token = "refresh-token-value"

    assert hash_token(token) == hash_token(token)
    assert hash_token(token) != hash_token("different-token-value")
