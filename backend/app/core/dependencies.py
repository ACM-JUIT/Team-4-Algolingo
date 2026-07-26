from __future__ import annotations

from typing import Annotated, Callable
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.core.security import ACCESS_TOKEN_TYPE, decode_token
from app.db.database import get_db_session
from app.models.enums import UserRole, UserStatus
from app.models.user import User

DBSession = Annotated[AsyncSession, Depends(get_db_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(session: DBSession, token: Annotated[str | None, Depends(oauth2_scheme)]) -> User:
    if not token:
        raise AppException(message="Not authenticated", status_code=401)

    payload = decode_token(token)
    if payload.get("type") != ACCESS_TOKEN_TYPE:
        raise AppException(message="Invalid access token", status_code=401)

    user_id = payload.get("sub")
    if not user_id:
        raise AppException(message="Invalid token payload", status_code=401)

    try:
        parsed_user_id = UUID(user_id)
    except ValueError as exc:
        raise AppException(message="Invalid token payload", status_code=401) from exc

    result = await session.execute(select(User).where(User.id == parsed_user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise AppException(message="User not found", status_code=401)

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.status != UserStatus.ACTIVE:
        raise AppException(message="User account is not active", status_code=403)
    return current_user


def require_roles(*allowed_roles: UserRole | str) -> Callable[..., User]:
    normalized_roles = {
        role if isinstance(role, UserRole) else UserRole(role)
        for role in allowed_roles
    }

    async def role_dependency(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
        if current_user.role not in normalized_roles:
            raise AppException(message="You do not have permission to access this resource", status_code=403)
        return current_user

    return role_dependency


CurrentUser = Annotated[User, Depends(get_current_active_user)]
