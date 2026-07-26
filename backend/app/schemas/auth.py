from __future__ import annotations

import re

from pydantic import EmailStr, Field, field_validator, model_validator

from app.schemas.base import ORMBaseSchema
from app.schemas.user import UserRead

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
PASSWORD_UPPERCASE_PATTERN = re.compile(r"[A-Z]")
PASSWORD_NUMBER_PATTERN = re.compile(r"\d")


class RegisterRequest(ORMBaseSchema):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.fullmatch(value):
            raise ValueError("Username must contain only letters, numbers, and underscores")
        return value

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not PASSWORD_UPPERCASE_PATTERN.search(value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not PASSWORD_NUMBER_PATTERN.search(value):
            raise ValueError("Password must contain at least one number")
        return value

    @model_validator(mode="after")
    def validate_password_match(self) -> "RegisterRequest":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class LoginRequest(ORMBaseSchema):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshTokenRequest(ORMBaseSchema):
    refresh_token: str = Field(min_length=20)


class LogoutRequest(ORMBaseSchema):
    refresh_token: str = Field(min_length=20)


class TokenPair(ORMBaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthSessionData(ORMBaseSchema):
    user: UserRead
    tokens: TokenPair


class CurrentUserData(ORMBaseSchema):
    user: UserRead


class LogoutData(ORMBaseSchema):
    logged_out: bool = True
