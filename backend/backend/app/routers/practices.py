from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.practice import (
    PracticeChallengeRead,
    PracticeSolutionRead,
    PracticeSubmissionRequest,
    PracticeSubmissionResult,
)
from app.services.practice_service import PracticeService

router = APIRouter(prefix="/practices", tags=["practices"])


@router.get(
    "/{practice_id}",
    response_model=ApiResponse[PracticeChallengeRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_practice(
    practice_id: UUID,
    session: DBSession,
    _: CurrentUser,
) -> ApiResponse[PracticeChallengeRead]:
    practice = await PracticeService.get_practice(session=session, practice_id=practice_id)
    return ApiResponse(message="Practice challenge fetched successfully", data=practice)


@router.post(
    "/{practice_id}/submit",
    response_model=ApiResponse[PracticeSubmissionResult],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def submit_practice(
    practice_id: UUID,
    payload: PracticeSubmissionRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[PracticeSubmissionResult]:
    result = await PracticeService.submit_practice(
        session=session,
        user=current_user,
        practice_id=practice_id,
        payload=payload,
    )
    return ApiResponse(message="Practice evaluated successfully", data=result)


@router.get(
    "/{practice_id}/solution",
    response_model=ApiResponse[PracticeSolutionRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_practice_solution(
    practice_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[PracticeSolutionRead]:
    solution = await PracticeService.get_solution(
        session=session,
        practice_id=practice_id,
        user_id=current_user.id,
    )
    return ApiResponse(message="Practice solution fetched successfully", data=solution)
