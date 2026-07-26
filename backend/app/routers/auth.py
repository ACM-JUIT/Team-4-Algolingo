from __future__ import annotations

from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.auth import (
    AuthSessionData,
    CurrentUserData,
    LoginRequest,
    LogoutData,
    LogoutRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.schemas.common import ApiResponse, ErrorResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=ApiResponse[AuthSessionData],
    responses={400: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
async def register(payload: RegisterRequest, session: DBSession) -> ApiResponse[AuthSessionData]:
    auth_session = await AuthService.register(session=session, payload=payload)
    return ApiResponse(message="Registration successful", data=auth_session)


@router.post(
    "/login",
    response_model=ApiResponse[AuthSessionData],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def login(payload: LoginRequest, session: DBSession) -> ApiResponse[AuthSessionData]:
    auth_session = await AuthService.login(session=session, payload=payload)
    return ApiResponse(message="Login successful", data=auth_session)


@router.post(
    "/refresh",
    response_model=ApiResponse[AuthSessionData],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def refresh_token(payload: RefreshTokenRequest, session: DBSession) -> ApiResponse[AuthSessionData]:
    auth_session = await AuthService.refresh(session=session, payload=payload)
    return ApiResponse(message="Token refreshed successfully", data=auth_session)


@router.get(
    "/me",
    response_model=ApiResponse[CurrentUserData],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def get_me(current_user: CurrentUser) -> ApiResponse[CurrentUserData]:
    user_data = await AuthService.get_current_user_data(current_user)
    return ApiResponse(message="Current user fetched successfully", data=CurrentUserData(user=user_data))


@router.post(
    "/logout",
    response_model=ApiResponse[LogoutData],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def logout(
    payload: LogoutRequest,
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[LogoutData]:
    logout_data = await AuthService.logout(
        session=session,
        user=current_user,
        refresh_token=payload.refresh_token,
    )
    return ApiResponse(message="Logout successful", data=logout_data)
