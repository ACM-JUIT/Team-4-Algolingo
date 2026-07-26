from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import RankTitle
from app.models.planet import Planet
from app.models.user import User
from app.models.user_progress import UserProgress


class RankService:
    """Calculates and synchronizes learner rank titles."""

    @staticmethod
    def determine_rank(
        *,
        level: int,
        completed_planet_orders: set[int],
        global_position: int | None = None,
    ) -> RankTitle:
        """Determines the rank title from level, completion state, and leaderboard rank."""
        has_planet_1 = 1 in completed_planet_orders
        has_planet_2 = 2 in completed_planet_orders
        has_planet_3 = 3 in completed_planet_orders
        all_mvp_complete = {1, 2, 3}.issubset(completed_planet_orders)

        if level >= 12 and all_mvp_complete and global_position is not None and global_position <= 50:
            return RankTitle.GALACTIC_LEGEND
        if level >= 9 and has_planet_3:
            return RankTitle.COMMANDER
        if level >= 6 and has_planet_2:
            return RankTitle.NAVIGATOR
        if level >= 3 and has_planet_1:
            return RankTitle.EXPLORER
        return RankTitle.CADET

    @staticmethod
    async def get_completed_planet_orders(session: AsyncSession, user_id: UUID) -> set[int]:
        """Returns completed planet order numbers for a learner."""
        result = await session.execute(
            select(Planet.order_number)
            .join(UserProgress, UserProgress.planet_id == Planet.id)
            .where(
                UserProgress.user_id == user_id,
                UserProgress.completed.is_(True),
            )
        )
        return {row[0] for row in result.all()}

    @staticmethod
    async def get_global_position(session: AsyncSession, user_id: UUID) -> int | None:
        """Returns the learner's global leaderboard position if available."""
        ranked_users = (
            select(
                User.id.label("user_id"),
                func.row_number().over(order_by=(User.xp.desc(), User.created_at.asc(), User.id.asc())).label("position"),
            )
            .subquery()
        )
        result = await session.execute(select(ranked_users.c.position).where(ranked_users.c.user_id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def sync_user_rank(cls, session: AsyncSession, user: User) -> RankTitle:
        """Synchronizes a user's stored rank title with current progression."""
        completed_planet_orders = await cls.get_completed_planet_orders(session=session, user_id=user.id)
        global_position = None
        if user.level >= 12 and {1, 2, 3}.issubset(completed_planet_orders):
            global_position = await cls.get_global_position(session=session, user_id=user.id)

        rank = cls.determine_rank(
            level=user.level,
            completed_planet_orders=completed_planet_orders,
            global_position=global_position,
        )
        user.rank_title = rank.value
        await session.flush()
        return rank
