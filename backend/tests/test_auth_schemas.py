from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.auth import RegisterRequest


def test_register_request_accepts_valid_payload() -> None:
    payload = RegisterRequest(
        username="captain_one",
        email="captain@example.com",
        password="StrongPass1",
        confirm_password="StrongPass1",
    )

    assert payload.username == "captain_one"


@pytest.mark.parametrize(
    ("password", "expected_message"),
    [
        ("weakpass1", "uppercase"),
        ("Weakpass", "number"),
    ],
)
def test_register_request_rejects_weak_passwords(password: str, expected_message: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(
            username="captain_one",
            email="captain@example.com",
            password=password,
            confirm_password=password,
        )

    assert expected_message in str(exc_info.value).lower()


def test_register_request_rejects_password_mismatch() -> None:
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(
            username="captain_one",
            email="captain@example.com",
            password="StrongPass1",
            confirm_password="StrongPass2",
        )

    assert "passwords do not match" in str(exc_info.value).lower()
