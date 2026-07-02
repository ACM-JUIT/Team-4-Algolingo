from __future__ import annotations

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.common import ApiResponse, ErrorResponse
from app.schemas.user import UserProfileRead, UserProfileUpdateRequest, UserRead
from app.services.user_service import UserService

router = APIRouter(tags=["users"])


@router.get(
    "/profile/{username}",
    response_model=ApiResponse[UserProfileRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_public_profile(
    username: str,
    session: DBSession,
    _: CurrentUser,
) -> ApiResponse[UserProfileRead]:
    profile = await UserService.get_public_profile(session=session, username=username)
    return ApiResponse(message="Profile fetched successfully", data=profile)


@router.patch(
    "/profile/me",
    response_model=ApiResponse[UserRead],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def update_my_profile(
    payload: UserProfileUpdateRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[UserRead]:
    updated_user = await UserService.update_profile(session=session, user=current_user, payload=payload)
    return ApiResponse(message="Profile updated successfully", data=updated_user)
