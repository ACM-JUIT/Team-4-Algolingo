from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.core.exceptions import AppException

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _build_token(
    *,
    subject: str,
    username: str,
    role: str,
    expires_delta: timedelta,
    token_type: str,
    jti: str | None = None,
) -> tuple[str, datetime]:
    issued_at = datetime.now(UTC)
    expires_at = issued_at + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "username": username,
        "role": role,
        "type": token_type,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    if jti:
        payload["jti"] = jti

    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, expires_at


def create_access_token(*, subject: str, username: str, role: str) -> tuple[str, datetime]:
    return _build_token(
        subject=subject,
        username=username,
        role=role,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type=ACCESS_TOKEN_TYPE,
    )


def create_refresh_token(*, subject: str, username: str, role: str) -> tuple[str, datetime, str]:
    refresh_jti = str(uuid4())
    token, expires_at = _build_token(
        subject=subject,
        username=username,
        role=role,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type=REFRESH_TOKEN_TYPE,
        jti=refresh_jti,
    )
    return token, expires_at, refresh_jti


def decode_token(token: str) -> dict[str, Any]:
    normalized_token = token.strip().strip('"').strip("'")
    try:
        return jwt.decode(normalized_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise AppException(message="Invalid or expired token", status_code=401) from exc


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_secure_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)
