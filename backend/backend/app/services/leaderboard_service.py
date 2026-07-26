from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.leaderboard_snapshot import LeaderboardSnapshot
from app.models.planet import Planet
from app.models.user import User
from app.models.user_progress import UserProgress
from app.schemas.enums import LeaderboardTypeEnum
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardQueryParams, LeaderboardRead, UserLeaderboardPosition


class LeaderboardService:
    @staticmethod
    def _paginate(page: int, limit: int) -> tuple[int, int]:
        offset = (page - 1) * limit
        return offset, limit

    @staticmethod
    def _entry_from_user_row(*, position: int, user_id: UUID, username: str, avatar_url: str | None, xp: int, level: int, rank_title: str) -> LeaderboardEntry:
        return LeaderboardEntry(
            position=position,
            user_id=user_id,
            username=username,
            avatar_url=avatar_url,
            xp=xp,
            level=level,
            rank_title=rank_title,
        )

    @classmethod
    async def get_leaderboard(
        cls,
        session: AsyncSession,
        *,
        params: LeaderboardQueryParams,
        current_user_id: UUID,
    ) -> LeaderboardRead:
        if params.type == LeaderboardTypeEnum.GLOBAL:
            return await cls._get_global_leaderboard(session=session, params=params, current_user_id=current_user_id)
        if params.type in {LeaderboardTypeEnum.WEEKLY, LeaderboardTypeEnum.MONTHLY}:
            return await cls._get_snapshot_leaderboard(session=session, params=params, current_user_id=current_user_id)
        if params.type == LeaderboardTypeEnum.GALAXY:
            if params.galaxy_id is None:
                raise AppException(message="galaxy_id is required for galaxy leaderboard", status_code=400)
            return await cls._get_galaxy_leaderboard(
                session=session,
                params=params,
                current_user_id=current_user_id,
                galaxy_id=params.galaxy_id,
            )
        raise AppException(message="Unsupported leaderboard type", status_code=400)

    @classmethod
    async def _get_global_leaderboard(
        cls,
        *,
        session: AsyncSession,
        params: LeaderboardQueryParams,
        current_user_id: UUID,
    ) -> LeaderboardRead:
        offset, limit = cls._paginate(params.page, params.limit)
        ranked_users = (
            select(
                User.id.label("user_id"),
                User.username.label("username"),
                User.avatar_url.label("avatar_url"),
                User.xp.label("xp"),
                User.level.label("level"),
                User.rank_title.label("rank_title"),
                func.row_number().over(order_by=(User.xp.desc(), User.created_at.asc(), User.id.asc())).label("position"),
            )
            .subquery()
        )

        total_result = await session.execute(select(func.count()).select_from(ranked_users))
        total = int(total_result.scalar_one() or 0)

        entries_result = await session.execute(
            select(ranked_users)
            .order_by(ranked_users.c.position.asc())
            .offset(offset)
            .limit(limit)
        )

        items = [
            cls._entry_from_user_row(
                position=row.position,
                user_id=row.user_id,
                username=row.username,
                avatar_url=row.avatar_url,
                xp=row.xp,
                level=row.level,
                rank_title=row.rank_title,
            )
            for row in entries_result.all()
        ]

        position_result = await session.execute(
            select(ranked_users.c.position, ranked_users.c.xp)
            .where(ranked_users.c.user_id == current_user_id)
        )
        position_row = position_result.one_or_none()

        return LeaderboardRead(
            leaderboard_type=params.type,
            items=items,
            page=params.page,
            limit=params.limit,
            total=total,
            snapshot_date=None,
            user_position=(
                None
                if position_row is None
                else UserLeaderboardPosition(
                    leaderboard_type=params.type,
                    position=position_row.position,
                    xp=position_row.xp,
                )
            ),
        )

    @classmethod
    async def _get_snapshot_leaderboard(
        cls,
        *,
        session: AsyncSession,
        params: LeaderboardQueryParams,
        current_user_id: UUID,
    ) -> LeaderboardRead:
        latest_date_result = await session.execute(
            select(func.max(LeaderboardSnapshot.snapshot_date)).where(
                LeaderboardSnapshot.leaderboard_type == params.type.value,
            )
        )
        snapshot_date = latest_date_result.scalar_one_or_none()
        if snapshot_date is None:
            return LeaderboardRead(
                leaderboard_type=params.type,
                items=[],
                page=params.page,
                limit=params.limit,
                total=0,
                snapshot_date=None,
                user_position=None,
            )

        offset, limit = cls._paginate(params.page, params.limit)

        total_result = await session.execute(
            select(func.count(LeaderboardSnapshot.id)).where(
                LeaderboardSnapshot.leaderboard_type == params.type.value,
                LeaderboardSnapshot.snapshot_date == snapshot_date,
            )
        )
        total = int(total_result.scalar_one() or 0)

        rows_result = await session.execute(
            select(LeaderboardSnapshot, User)
            .join(User, User.id == LeaderboardSnapshot.user_id)
            .where(
                LeaderboardSnapshot.leaderboard_type == params.type.value,
                LeaderboardSnapshot.snapshot_date == snapshot_date,
            )
            .order_by(LeaderboardSnapshot.rank_position.asc())
            .offset(offset)
            .limit(limit)
        )
        items = [
            cls._entry_from_user_row(
                position=snapshot.rank_position,
                user_id=user.id,
                username=user.username,
                avatar_url=user.avatar_url,
                xp=snapshot.xp,
                level=user.level,
                rank_title=user.rank_title,
            )
            for snapshot, user in rows_result.all()
        ]

        position_result = await session.execute(
            select(LeaderboardSnapshot.rank_position, LeaderboardSnapshot.xp)
            .where(
                LeaderboardSnapshot.leaderboard_type == params.type.value,
                LeaderboardSnapshot.snapshot_date == snapshot_date,
                LeaderboardSnapshot.user_id == current_user_id,
            )
        )
        position_row = position_result.one_or_none()

        return LeaderboardRead(
            leaderboard_type=params.type,
            items=items,
            page=params.page,
            limit=params.limit,
            total=total,
            snapshot_date=snapshot_date,
            user_position=(
                None
                if position_row is None
                else UserLeaderboardPosition(
                    leaderboard_type=params.type,
                    position=position_row.rank_position,
                    xp=position_row.xp,
                )
            ),
        )

    @classmethod
    async def _get_galaxy_leaderboard(
        cls,
        *,
        session: AsyncSession,
        params: LeaderboardQueryParams,
        current_user_id: UUID,
        galaxy_id: UUID,
    ) -> LeaderboardRead:
        galaxy_exists_result = await session.execute(select(func.count(Planet.id)).where(Planet.galaxy_id == galaxy_id))
        if int(galaxy_exists_result.scalar_one() or 0) == 0:
            raise AppException(message="Galaxy not found", status_code=404)

        user_galaxy_xp = (
            select(
                UserProgress.user_id.label("user_id"),
                func.coalesce(func.sum(UserProgress.xp_earned), 0).label("xp"),
            )
            .join(Planet, Planet.id == UserProgress.planet_id)
            .where(Planet.galaxy_id == galaxy_id)
            .group_by(UserProgress.user_id)
            .subquery()
        )

        ranked_users = (
            select(
                User.id.label("user_id"),
                User.username.label("username"),
                User.avatar_url.label("avatar_url"),
                user_galaxy_xp.c.xp.label("xp"),
                User.level.label("level"),
                User.rank_title.label("rank_title"),
                func.row_number().over(
                    order_by=(user_galaxy_xp.c.xp.desc(), User.created_at.asc(), User.id.asc())
                ).label("position"),
            )
            .join(user_galaxy_xp, user_galaxy_xp.c.user_id == User.id)
            .subquery()
        )

        offset, limit = cls._paginate(params.page, params.limit)
        total_result = await session.execute(select(func.count()).select_from(ranked_users))
        total = int(total_result.scalar_one() or 0)

        rows_result = await session.execute(
            select(ranked_users)
            .order_by(ranked_users.c.position.asc())
            .offset(offset)
            .limit(limit)
        )
        items = [
            cls._entry_from_user_row(
                position=row.position,
                user_id=row.user_id,
                username=row.username,
                avatar_url=row.avatar_url,
                xp=row.xp,
                level=row.level,
                rank_title=row.rank_title,
            )
            for row in rows_result.all()
        ]

        position_result = await session.execute(
            select(ranked_users.c.position, ranked_users.c.xp)
            .where(ranked_users.c.user_id == current_user_id)
        )
        position_row = position_result.one_or_none()

        return LeaderboardRead(
            leaderboard_type=params.type,
            items=items,
            page=params.page,
            limit=params.limit,
            total=total,
            snapshot_date=None,
            user_position=(
                None
                if position_row is None
                else UserLeaderboardPosition(
                    leaderboard_type=params.type,
                    position=position_row.position,
                    xp=position_row.xp,
                )
            ),
        )
