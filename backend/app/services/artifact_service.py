from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.models.artifact import Artifact
from app.models.enums import EventType
from app.models.user import User
from app.models.user_artifact import UserArtifact
from app.schemas.artifact import ArtifactCollectionItem, ArtifactRead, ArtifactSummary, UserArtifactRead
from app.services.event_service import EventService
from app.services.xp_service import XPService


class ArtifactService:
    """Handles artifact serialization, inventory reads, and planet artifact unlocking."""

    @staticmethod
    def serialize_summary(artifact: Artifact) -> ArtifactSummary:
        """Builds a compact artifact response object."""
        return ArtifactSummary(
            id=artifact.id,
            name=artifact.name,
            rarity=artifact.rarity,
            category=artifact.category,
            xp_bonus_percent=artifact.xp_bonus_percent,
            icon_url=artifact.icon_url,
            is_hidden=artifact.is_hidden,
        )

    @classmethod
    def serialize_artifact(cls, artifact: Artifact) -> ArtifactRead:
        """Builds a detailed artifact response object."""
        return ArtifactRead(
            id=artifact.id,
            name=artifact.name,
            description=artifact.description,
            rarity=artifact.rarity,
            rarity_color=artifact.rarity_color,
            category=artifact.category,
            unlock_condition=artifact.unlock_condition,
            xp_bonus_percent=artifact.xp_bonus_percent,
            icon_url=artifact.icon_url,
            display_order=artifact.display_order,
            is_hidden=artifact.is_hidden,
            created_at=artifact.created_at,
            updated_at=artifact.updated_at,
        )

    @classmethod
    def serialize_user_artifact(cls, user_artifact: UserArtifact) -> UserArtifactRead:
        """Builds a user-specific collected artifact response."""
        return UserArtifactRead(
            id=user_artifact.id,
            user_id=user_artifact.user_id,
            artifact_id=user_artifact.artifact_id,
            showcased=user_artifact.showcased,
            unlocked_at=user_artifact.unlocked_at,
            artifact=cls.serialize_summary(user_artifact.artifact),
        )

    @staticmethod
    async def is_artifact_collected(session: AsyncSession, *, user_id: UUID, artifact_id: UUID) -> bool:
        """Returns whether a user has already collected a specific artifact."""
        result = await session.execute(
            select(func.count(UserArtifact.id)).where(
                UserArtifact.user_id == user_id,
                UserArtifact.artifact_id == artifact_id,
            )
        )
        return int(result.scalar_one() or 0) > 0

    @classmethod
    async def unlock_artifact(
        cls,
        session: AsyncSession,
        *,
        user: User,
        artifact: Artifact,
        bonus_percent_override: int | None = None,
    ) -> ArtifactSummary | None:
        """Unlocks one artifact exactly once and applies its rarity XP reward."""
        already_collected = await cls.is_artifact_collected(session=session, user_id=user.id, artifact_id=artifact.id)
        if already_collected:
            return None

        user_artifact = UserArtifact(
            user_id=user.id,
            artifact_id=artifact.id,
            showcased=False,
        )
        session.add(user_artifact)
        await session.flush()

        base_xp = XPService.get_artifact_unlock_base_xp(artifact.rarity)
        if base_xp > 0:
            await XPService.award_user_xp(
                session=session,
                user=user,
                base_xp=base_xp,
                bonus_percent_override=bonus_percent_override,
            )

        await EventService.track_event(
            session=session,
            user_id=user.id,
            event_type=EventType.ARTIFACT_UNLOCKED,
            event_data={
                "artifact_id": str(artifact.id),
                "artifact_name": artifact.name,
                "rarity": artifact.rarity,
            },
        )
        return cls.serialize_summary(artifact)

    @classmethod
    async def unlock_planet_artifact(
        cls,
        session: AsyncSession,
        *,
        user: User,
        artifact: Artifact | None,
        bonus_percent_override: int | None = None,
    ) -> ArtifactSummary | None:
        """Unlocks the single MVP planet artifact associated with a completed planet."""
        if artifact is None:
            return None
        return await cls.unlock_artifact(
            session=session,
            user=user,
            artifact=artifact,
            bonus_percent_override=bonus_percent_override,
        )

    @classmethod
    async def list_artifacts(cls, session: AsyncSession, user_id: UUID) -> list[ArtifactCollectionItem]:
        """Returns the full artifact catalog with user collection state."""
        artifact_result = await session.execute(
            select(Artifact).order_by(Artifact.display_order.asc(), Artifact.name.asc())
        )
        artifacts = artifact_result.scalars().all()

        user_artifact_result = await session.execute(
            select(UserArtifact)
            .options(selectinload(UserArtifact.artifact))
            .where(UserArtifact.user_id == user_id)
        )
        user_artifacts = {row.artifact_id: row for row in user_artifact_result.scalars().all()}

        return [
            ArtifactCollectionItem(
                artifact=cls.serialize_artifact(artifact),
                collected=artifact.id in user_artifacts,
                showcased=user_artifacts[artifact.id].showcased if artifact.id in user_artifacts else False,
                unlocked_at=user_artifacts[artifact.id].unlocked_at if artifact.id in user_artifacts else None,
            )
            for artifact in artifacts
        ]

    @classmethod
    async def get_artifact(cls, session: AsyncSession, artifact_id: UUID) -> ArtifactRead:
        """Returns a single artifact by identifier."""
        artifact = await session.get(Artifact, artifact_id)
        if artifact is None:
            raise AppException(message="Artifact not found", status_code=404)
        return cls.serialize_artifact(artifact)

    @classmethod
    async def list_user_artifacts(cls, session: AsyncSession, user_id: UUID) -> list[UserArtifactRead]:
        """Returns artifacts earned by a specific user."""
        user = await session.get(User, user_id)
        if user is None:
            raise AppException(message="User not found", status_code=404)

        result = await session.execute(
            select(UserArtifact)
            .options(selectinload(UserArtifact.artifact))
            .where(UserArtifact.user_id == user_id)
            .order_by(UserArtifact.unlocked_at.desc())
        )
        return [cls.serialize_user_artifact(row) for row in result.scalars().all()]
