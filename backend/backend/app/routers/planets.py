from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.planet import PlanetDetail
from app.services.planet_service import PlanetService

router = APIRouter(prefix="/planets", tags=["planets"])


@router.get(
    "/{planet_id}",
    response_model=ApiResponse[PlanetDetail],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_planet_detail(
    planet_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[PlanetDetail]:
    planet = await PlanetService.get_planet_detail(session=session, planet_id=planet_id, user_id=current_user.id)
    return ApiResponse(message="Planet fetched successfully", data=planet)
