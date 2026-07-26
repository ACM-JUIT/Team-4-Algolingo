from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.galaxy import GalaxyDetail, GalaxyExplorerItem
from app.services.galaxy_service import GalaxyService

router = APIRouter(prefix="/galaxies", tags=["galaxies"])


@router.get(
    "",
    response_model=ApiResponse[list[GalaxyExplorerItem]],
    responses={401: {"model": ErrorResponse}},
)
async def list_galaxies(
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[list[GalaxyExplorerItem]]:
    galaxies = await GalaxyService.list_galaxies(session=session, user_id=current_user.id)
    return ApiResponse(message="Galaxies fetched successfully", data=galaxies)


@router.get(
    "/{galaxy_id}",
    response_model=ApiResponse[GalaxyDetail],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_galaxy_detail(
    galaxy_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[GalaxyDetail]:
    galaxy = await GalaxyService.get_galaxy_detail(session=session, galaxy_id=galaxy_id, user_id=current_user.id)
    return ApiResponse(message="Galaxy fetched successfully", data=galaxy)
