from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.quiz import QuizQuestionRead, QuizSubmitRequest, QuizSubmitResult
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/planets", tags=["quizzes"])


@router.get(
    "/{planet_id}/quiz",
    response_model=ApiResponse[list[QuizQuestionRead]],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    summary="Get Planet Quiz",
    description="Returns quiz questions for a planet without exposing correct answers.",
    response_description="Quiz questions retrieved successfully.",
)
async def get_planet_quiz(
    planet_id: UUID,
    session: DBSession,
    _: CurrentUser,
) -> ApiResponse[list[QuizQuestionRead]]:
    questions = await QuizService.get_quiz_questions(session=session, planet_id=planet_id)
    return ApiResponse(message="Quiz fetched successfully", data=questions)


@router.post(
    "/{planet_id}/quiz/submit",
    response_model=ApiResponse[QuizSubmitResult],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    summary="Submit Planet Quiz",
    description="Grades a quiz submission for a planet and applies the resulting progression updates.",
    response_description="Quiz submission processed successfully.",
)
async def submit_quiz(
    planet_id: UUID,
    payload: QuizSubmitRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[QuizSubmitResult]:
    result = await QuizService.submit_quiz(
        session=session,
        user=current_user,
        planet_id=planet_id,
        submitted_answers=payload.answers,
    )
    return ApiResponse(message="Quiz submitted successfully", data=result)
