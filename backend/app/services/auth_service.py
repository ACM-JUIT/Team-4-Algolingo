from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.core.security import (
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.models.enums import UserRole, UserStatus
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import AuthSessionData, LoginRequest, LogoutData, RefreshTokenRequest, RegisterRequest, TokenPair
from app.schemas.user import UserRead
from app.services.rank_service import RankService
from app.services.xp_service import XPService

logger = logging.getLogger(__name__)
settings = get_settings()

ACTIVE_STATUS = UserStatus.ACTIVE
USER_ROLE = UserRole.USER
ACCESS_TOKEN_EXPIRES_IN_SECONDS = settings.access_token_expire_minutes * 60


@dataclass(slots=True)
class StreakState:
    streak_days: int
    last_login_date: date
    first_login_today: bool


class AuthService:
    @staticmethod
    def _now_utc() -> datetime:
        return datetime.now(UTC)

    @staticmethod
    def _assume_utc(timestamp: datetime) -> datetime:
        return timestamp if timestamp.tzinfo is not None else timestamp.replace(tzinfo=UTC)

    @staticmethod
    def calculate_streak(last_login_date: date | None, current_streak: int, today: date | None = None) -> StreakState:
        current_date = today or AuthService._now_utc().date()

        if last_login_date is None:
            return StreakState(streak_days=1, last_login_date=current_date, first_login_today=True)

        if last_login_date == current_date:
            return StreakState(
                streak_days=max(current_streak, 1),
                last_login_date=current_date,
                first_login_today=False,
            )

        if last_login_date.toordinal() == current_date.toordinal() - 1:
            return StreakState(
                streak_days=max(current_streak, 0) + 1,
                last_login_date=current_date,
                first_login_today=True,
            )

        return StreakState(streak_days=1, last_login_date=current_date, first_login_today=True)

    @classmethod
    async def register(cls, session: AsyncSession, payload: RegisterRequest) -> AuthSessionData:
        existing_user = await cls._get_user_by_email_or_username(
            session=session,
            email=payload.email,
            username=payload.username,
        )
        if existing_user is not None:
            if existing_user.email.lower() == payload.email.lower():
                raise AppException(message="Email is already registered", status_code=409)
            raise AppException(message="Username is already taken", status_code=409)

        streak_state = cls.calculate_streak(last_login_date=None, current_streak=0)

        user = User(
            username=payload.username,
            email=payload.email.lower(),
            password_hash=hash_password(payload.password),
            status=ACTIVE_STATUS,
            role=USER_ROLE,
            streak_days=streak_state.streak_days,
            last_login_date=streak_state.last_login_date,
        )

        try:
            session.add(user)
            await session.flush()

            await cls._process_login_rewards(session=session, user=user, streak_state=streak_state)
            auth_session = await cls._issue_tokens(session=session, user=user)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

        await session.refresh(user)

        logger.info("New user registered", extra={"user_id": str(user.id), "username": user.username})
        return auth_session

    @classmethod
    async def login(cls, session: AsyncSession, payload: LoginRequest) -> AuthSessionData:
        user = await cls._get_user_by_email(session=session, email=payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise AppException(message="Invalid email or password", status_code=401)

        if user.status != ACTIVE_STATUS:
            raise AppException(message="User account is not active", status_code=403)

        streak_state = cls.calculate_streak(user.last_login_date, user.streak_days)
        user.streak_days = streak_state.streak_days
        user.last_login_date = streak_state.last_login_date

        try:
            await cls._process_login_rewards(session=session, user=user, streak_state=streak_state)
            auth_session = await cls._issue_tokens(session=session, user=user)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

        await session.refresh(user)

        logger.info("User logged in", extra={"user_id": str(user.id), "username": user.username})
        return auth_session

    @classmethod
    async def refresh(cls, session: AsyncSession, payload: RefreshTokenRequest) -> AuthSessionData:
        token_payload = decode_token(payload.refresh_token)
        if token_payload.get("type") != REFRESH_TOKEN_TYPE:
            raise AppException(message="Invalid refresh token", status_code=401)

        refresh_token_hash = hash_token(payload.refresh_token)
        refresh_token_record = await cls._get_active_refresh_token(session=session, token_hash=refresh_token_hash)
        if refresh_token_record is None:
            raise AppException(message="Refresh token is invalid or revoked", status_code=401)

        if cls._assume_utc(refresh_token_record.expires_at) < cls._now_utc():
            refresh_token_record.revoked = True
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            raise AppException(message="Refresh token has expired", status_code=401)

        try:
            user_id = UUID(token_payload["sub"])
        except (KeyError, ValueError) as exc:
            raise AppException(message="Invalid refresh token", status_code=401) from exc

        user = await session.get(User, user_id)
        if user is None or user.status != ACTIVE_STATUS:
            raise AppException(message="User account is not active", status_code=403)

        try:
            refresh_token_record.revoked = True
            auth_session = await cls._issue_tokens(session=session, user=user)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

        await session.refresh(user)

        logger.info("Refresh token rotated", extra={"user_id": str(user.id), "username": user.username})
        return auth_session

    @classmethod
    async def logout(cls, session: AsyncSession, user: User, refresh_token: str) -> LogoutData:
        token_hash_value = hash_token(refresh_token)
        token_record = await cls._get_active_refresh_token(session=session, token_hash=token_hash_value)

        if token_record is not None and str(token_record.user_id) == str(user.id):
            token_record.revoked = True
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            logger.info("User logged out", extra={"user_id": str(user.id), "username": user.username})

        return LogoutData(logged_out=True)

    @staticmethod
    async def get_current_user_data(user: User) -> UserRead:
        return UserRead.model_validate(user)

    @classmethod
    async def _process_login_rewards(
        cls,
        *,
        session: AsyncSession,
        user: User,
        streak_state: StreakState,
    ) -> None:
        daily_login_award = await XPService.process_daily_login(
            session=session,
            user=user,
            streak_day=streak_state.streak_days,
            login_date=streak_state.last_login_date,
        )
        if daily_login_award is not None:
            await RankService.sync_user_rank(session=session, user=user)

    @classmethod
    async def _issue_tokens(cls, session: AsyncSession, user: User) -> AuthSessionData:
        access_token, _ = create_access_token(
            subject=str(user.id),
            username=user.username,
            role=user.role,
        )
        refresh_token, refresh_expires_at, _ = create_refresh_token(
            subject=str(user.id),
            username=user.username,
            role=user.role,
        )

        refresh_token_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=refresh_expires_at.replace(tzinfo=None),
            revoked=False,
        )
        session.add(refresh_token_record)
        await session.flush()

        return AuthSessionData(
            user=UserRead.model_validate(user),
            tokens=TokenPair(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=ACCESS_TOKEN_EXPIRES_IN_SECONDS,
            ),
        )

    @staticmethod
    async def _get_user_by_email(session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    @staticmethod
    async def _get_user_by_email_or_username(session: AsyncSession, email: str, username: str) -> User | None:
        result = await session.execute(
            select(User).where(
                or_(User.email == email.lower(), User.username == username),
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def _get_active_refresh_token(session: AsyncSession, token_hash: str) -> RefreshToken | None:
        result = await session.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked.is_(False),
            )
        )
        return result.scalar_one_or_none()
