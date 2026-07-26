from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.discovery import DiscoveryCompletionResult, DiscoveryRead
from app.services.discovery_service import DiscoveryService
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/discoveries", tags=["discoveries"])


@router.get(
    "/{discovery_id}",
    response_model=ApiResponse[DiscoveryRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_discovery(
    discovery_id: UUID,
    session: DBSession,
    _: CurrentUser,
) -> ApiResponse[DiscoveryRead]:
    discovery = await DiscoveryService.get_discovery(session=session, discovery_id=discovery_id)
    return ApiResponse(message="Discovery fetched successfully", data=discovery)


@router.post(
    "/{discovery_id}/complete",
    response_model=ApiResponse[DiscoveryCompletionResult],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
)
async def complete_discovery(
    discovery_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[DiscoveryCompletionResult]:
    result = await ProgressService.complete_discovery(
        session=session,
        user=current_user,
        discovery_id=discovery_id,
    )
    return ApiResponse(message="Discovery completed successfully", data=result)
