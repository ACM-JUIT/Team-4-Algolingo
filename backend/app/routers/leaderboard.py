from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.enums import LeaderboardTypeEnum
from app.schemas.leaderboard import LeaderboardQueryParams, LeaderboardRead
from app.services.leaderboard_service import LeaderboardService

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


async def get_leaderboard_query_params(
    type: LeaderboardTypeEnum = Query(default=LeaderboardTypeEnum.GLOBAL),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=50),
    galaxy_id: UUID | None = Query(default=None),
) -> LeaderboardQueryParams:
    return LeaderboardQueryParams(type=type, page=page, limit=limit, galaxy_id=galaxy_id)


@router.get(
    "",
    response_model=ApiResponse[LeaderboardRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_leaderboard(
    session: DBSession,
    current_user: CurrentUser,
    params: Annotated[LeaderboardQueryParams, Depends(get_leaderboard_query_params)],
) -> ApiResponse[LeaderboardRead]:
    leaderboard = await LeaderboardService.get_leaderboard(
        session=session,
        params=params,
        current_user_id=current_user.id,
    )
    return ApiResponse(message="Leaderboard fetched successfully", data=leaderboard)
