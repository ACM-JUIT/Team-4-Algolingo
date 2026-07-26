from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.quiz import QuizQuestionRead, QuizSubmitRequest, QuizSubmitResult
from app.services.quiz_service import QuizService

router = APIRouter(tags=["quizzes"])


async def _build_quiz_questions_response(
    *,
    planet_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[list[QuizQuestionRead]]:
    questions = await QuizService.get_quiz_questions_for_user(
        session=session,
        planet_id=planet_id,
        user_id=current_user.id,
    )
    return ApiResponse(message="Quiz fetched successfully", data=questions)


async def _build_quiz_submission_response(
    *,
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


@router.get(
    "/planets/{planet_id}/quiz",
    response_model=ApiResponse[list[QuizQuestionRead]],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    summary="Get Planet Quiz",
    description="Returns quiz questions for a planet without exposing correct answers.",
    response_description="Quiz questions retrieved successfully.",
)
async def get_planet_quiz(
    planet_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[list[QuizQuestionRead]]:
    return await _build_quiz_questions_response(
        planet_id=planet_id,
        session=session,
        current_user=current_user,
    )


@router.get(
    "/quizzes/{planet_id}",
    response_model=ApiResponse[list[QuizQuestionRead]],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    summary="Get Quiz",
    description="Compatibility alias for fetching quiz questions by planet identifier.",
    response_description="Quiz questions retrieved successfully.",
)
async def get_quiz(
    planet_id: UUID,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[list[QuizQuestionRead]]:
    return await _build_quiz_questions_response(
        planet_id=planet_id,
        session=session,
        current_user=current_user,
    )


@router.post(
    "/planets/{planet_id}/quiz/submit",
    response_model=ApiResponse[QuizSubmitResult],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    summary="Submit Planet Quiz",
    description="Grades a quiz submission for a planet and applies the resulting progression updates.",
    response_description="Quiz submission processed successfully.",
)
async def submit_planet_quiz(
    planet_id: UUID,
    payload: QuizSubmitRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[QuizSubmitResult]:
    return await _build_quiz_submission_response(
        planet_id=planet_id,
        payload=payload,
        session=session,
        current_user=current_user,
    )


@router.post(
    "/quizzes/{planet_id}/submit",
    response_model=ApiResponse[QuizSubmitResult],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    summary="Submit Quiz",
    description="Compatibility alias for submitting a planet quiz by planet identifier.",
    response_description="Quiz submission processed successfully.",
)
async def submit_quiz(
    planet_id: UUID,
    payload: QuizSubmitRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[QuizSubmitResult]:
    return await _build_quiz_submission_response(
        planet_id=planet_id,
        payload=payload,
        session=session,
        current_user=current_user,
    )
