from __future__ import annotations

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.dashboard import DashboardRead
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "",
    response_model=ApiResponse[DashboardRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_dashboard(
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[DashboardRead]:
    dashboard = await DashboardService.get_dashboard(session=session, user_id=current_user.id)
    return ApiResponse(message="Dashboard fetched successfully", data=dashboard)
