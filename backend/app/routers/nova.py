from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.nova import (
    NovaAskRequest,
    NovaDebugRequest,
    NovaHintRequest,
    NovaRecommendRequest,
    NovaResponseData,
)
from app.services.nova_service import NovaService

router = APIRouter(prefix="/nova", tags=["nova"])


@router.post(
    "/ask",
    response_model=ApiResponse[NovaResponseData],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 429: {"model": ErrorResponse}, 502: {"model": ErrorResponse}, 504: {"model": ErrorResponse}},
)
async def ask_nova(
    payload: NovaAskRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[NovaResponseData]:
    response = await NovaService.ask(session=session, user=current_user, payload=payload)
    return ApiResponse(message="NOVA response generated successfully", data=response)


@router.post(
    "/hint/{practice_id}",
    response_model=ApiResponse[NovaResponseData],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 429: {"model": ErrorResponse}, 502: {"model": ErrorResponse}, 504: {"model": ErrorResponse}},
)
async def nova_hint(
    practice_id: UUID,
    payload: NovaHintRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[NovaResponseData]:
    response = await NovaService.hint(
        session=session,
        user=current_user,
        practice_id=practice_id,
        payload=payload,
    )
    return ApiResponse(message="NOVA hint generated successfully", data=response)


@router.post(
    "/debug",
    response_model=ApiResponse[NovaResponseData],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 429: {"model": ErrorResponse}, 502: {"model": ErrorResponse}, 504: {"model": ErrorResponse}},
)
async def nova_debug(
    payload: NovaDebugRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[NovaResponseData]:
    response = await NovaService.debug(session=session, user=current_user, payload=payload)
    return ApiResponse(message="NOVA debug response generated successfully", data=response)


@router.post(
    "/recommend",
    response_model=ApiResponse[NovaResponseData],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 429: {"model": ErrorResponse}, 502: {"model": ErrorResponse}, 504: {"model": ErrorResponse}},
)
async def nova_recommend(
    payload: NovaRecommendRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[NovaResponseData]:
    response = await NovaService.recommend(session=session, user=current_user, payload=payload)
    return ApiResponse(message="NOVA recommendation generated successfully", data=response)
