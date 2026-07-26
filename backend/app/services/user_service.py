from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.user import User
from app.models.user_artifact import UserArtifact
from app.models.user_progress import UserProgress
from app.schemas.user import UserProfileRead, UserProfileStats, UserProfileUpdateRequest, UserPublicProfile, UserRead
from app.services.service_utils import ensure_string_list


class UserService:
    """Handles user lookup, profile updates, and public profile summaries."""

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: UUID) -> User | None:
        """Returns a user by identifier if present."""
        return await session.get(User, user_id)

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> User | None:
        """Returns a user by username if present."""
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @classmethod
    async def get_public_profile(cls, session: AsyncSession, username: str) -> UserProfileRead:
        """Returns a user's public profile and aggregate learning stats."""
        user = await cls.get_by_username(session=session, username=username)
        if user is None:
            raise AppException(message="User not found", status_code=404)

        stats = await cls._build_profile_stats(session=session, user_id=user.id)
        return UserProfileRead(
            user=UserPublicProfile.model_validate(user),
            stats=stats,
        )

    @staticmethod
    async def update_profile(session: AsyncSession, user: User, payload: UserProfileUpdateRequest) -> UserRead:
        """Applies profile updates for the authenticated user."""
        if "avatar_url" in payload.model_fields_set:
            user.avatar_url = payload.avatar_url
        if "bio" in payload.model_fields_set:
            user.bio = payload.bio

        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        await session.refresh(user)
        return UserRead.model_validate(user)

    @classmethod
    async def _build_profile_stats(cls, session: AsyncSession, user_id: UUID) -> UserProfileStats:
        progress_result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
        progress_rows = progress_result.scalars().all()

        artifact_result = await session.execute(select(UserArtifact).where(UserArtifact.user_id == user_id))
        artifact_rows = artifact_result.scalars().all()

        return cls.build_profile_stats(
            progress_rows=progress_rows,
            artifacts_count=len(artifact_rows),
        )

    @staticmethod
    def build_profile_stats(*, progress_rows: list[UserProgress], artifacts_count: int) -> UserProfileStats:
        """Builds aggregate profile statistics from progress rows and artifact count."""
        completed_planets = sum(1 for row in progress_rows if row.completed)
        quizzes_passed = sum(1 for row in progress_rows if row.quiz_passed)
        completed_discoveries = sum(len(ensure_string_list(row.completed_discoveries)) for row in progress_rows)
        completed_practices = sum(len(ensure_string_list(row.completed_practices)) for row in progress_rows)

        return UserProfileStats(
            completed_planets=completed_planets,
            completed_discoveries=completed_discoveries,
            completed_practices=completed_practices,
            quizzes_passed=quizzes_passed,
            artifacts_earned=artifacts_count,
        )
