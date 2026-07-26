from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.artifact import Artifact
from app.models.daily_login import DailyLogin
from app.models.enums import ArtifactRarity
from app.models.user import User
from app.models.user_artifact import UserArtifact
from app.services.level_service import LevelService

DAILY_LOGIN_BASE_XP = 25
THREE_DAY_STREAK_BONUS_XP = 50
SEVEN_DAY_STREAK_BONUS_XP = 100
THIRTY_DAY_STREAK_BONUS_XP = 500
PLANET_COMPLETION_BONUS_XP = 200
ARTIFACT_UNLOCK_XP_BY_RARITY = {
    ArtifactRarity.COMMON: 50,
    ArtifactRarity.RARE: 150,
    ArtifactRarity.EPIC: 500,
    ArtifactRarity.LEGENDARY: 1000,
}


@dataclass(slots=True)
class XPAwardResult:
    base_xp: int
    bonus_percent: int
    bonus_xp: int
    total_xp: int
    new_total_xp: int
    new_level: int


class XPService:
    """Centralizes XP calculations and XP-side effects."""

    @staticmethod
    def calculate_bonus_xp(base_xp: int, bonus_percent: int) -> int:
        """Calculates additive artifact bonus XP for a base reward."""
        if base_xp <= 0 or bonus_percent <= 0:
            return 0
        raw_bonus = (Decimal(base_xp) * Decimal(bonus_percent)) / Decimal("100")
        return int(raw_bonus.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    @classmethod
    def build_award_result(cls, *, current_xp: int, base_xp: int, bonus_percent: int) -> XPAwardResult:
        """Builds the full XP award outcome including level recalculation."""
        bonus_xp = cls.calculate_bonus_xp(base_xp, bonus_percent)
        total_xp = base_xp + bonus_xp
        new_total_xp = current_xp + total_xp
        new_level = LevelService.determine_level(new_total_xp)
        return XPAwardResult(
            base_xp=base_xp,
            bonus_percent=bonus_percent,
            bonus_xp=bonus_xp,
            total_xp=total_xp,
            new_total_xp=new_total_xp,
            new_level=new_level,
        )

    @staticmethod
    async def get_total_artifact_bonus_percent(session: AsyncSession, user_id: UUID) -> int:
        result = await session.execute(
            select(func.coalesce(func.sum(Artifact.xp_bonus_percent), 0))
            .select_from(UserArtifact)
            .join(Artifact, Artifact.id == UserArtifact.artifact_id)
            .where(UserArtifact.user_id == user_id)
        )
        return int(result.scalar_one() or 0)

    @classmethod
    async def award_user_xp(
        cls,
        session: AsyncSession,
        *,
        user: User,
        base_xp: int,
        bonus_percent_override: int | None = None,
    ) -> XPAwardResult:
        """Applies XP to a user and synchronizes the resulting level."""
        bonus_percent = (
            bonus_percent_override
            if bonus_percent_override is not None
            else await cls.get_total_artifact_bonus_percent(session=session, user_id=user.id)
        )
        award = cls.build_award_result(current_xp=user.xp, base_xp=base_xp, bonus_percent=bonus_percent)
        user.xp = award.new_total_xp
        user.level = award.new_level
        await session.flush()
        return award

    @staticmethod
    def determine_streak_bonus(streak_day: int) -> int:
        if streak_day > 0 and streak_day % 30 == 0:
            return THIRTY_DAY_STREAK_BONUS_XP
        if streak_day > 0 and streak_day % 7 == 0:
            return SEVEN_DAY_STREAK_BONUS_XP
        if streak_day > 0 and streak_day % 3 == 0:
            return THREE_DAY_STREAK_BONUS_XP
        return 0

    @classmethod
    async def process_daily_login(
        cls,
        session: AsyncSession,
        *,
        user: User,
        streak_day: int,
        login_date: date | None = None,
    ) -> XPAwardResult | None:
        """Processes once-per-day login XP and streak bonuses."""
        effective_date = login_date or datetime.now(UTC).date()
        existing_result = await session.execute(
            select(DailyLogin).where(
                DailyLogin.user_id == user.id,
                DailyLogin.login_date == effective_date,
            )
        )
        existing_login = existing_result.scalar_one_or_none()
        if existing_login is not None:
            return None

        base_xp = DAILY_LOGIN_BASE_XP + cls.determine_streak_bonus(streak_day)
        current_bonus_percent = await cls.get_total_artifact_bonus_percent(session=session, user_id=user.id)
        award = await cls.award_user_xp(
            session=session,
            user=user,
            base_xp=base_xp,
            bonus_percent_override=current_bonus_percent,
        )

        session.add(
            DailyLogin(
                user_id=user.id,
                login_date=effective_date,
                xp_earned=award.total_xp,
                streak_day=streak_day,
            )
        )
        await session.flush()
        return award

    @staticmethod
    def get_artifact_unlock_base_xp(rarity: ArtifactRarity | str) -> int:
        """Returns the base XP granted when unlocking an artifact by rarity."""
        normalized_rarity = rarity if isinstance(rarity, ArtifactRarity) else ArtifactRarity(rarity)
        return ARTIFACT_UNLOCK_XP_BY_RARITY.get(normalized_rarity, 0)
