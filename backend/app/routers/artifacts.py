from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.artifact import ArtifactCollectionItem, ArtifactRead, UserArtifactRead
from app.schemas.common import ApiResponse, ErrorResponse
from app.services.artifact_service import ArtifactService

router = APIRouter(tags=["artifacts"])


@router.get(
    "/artifacts",
    response_model=ApiResponse[list[ArtifactCollectionItem]],
    responses={401: {"model": ErrorResponse}},
)
async def list_artifacts(
    session: DBSession,
    current_user: CurrentUser,
) -> ApiResponse[list[ArtifactCollectionItem]]:
    artifacts = await ArtifactService.list_artifacts(session=session, user_id=current_user.id)
    return ApiResponse(message="Artifacts fetched successfully", data=artifacts)


@router.get(
    "/artifacts/{artifact_id}",
    response_model=ApiResponse[ArtifactRead],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_artifact(
    artifact_id: UUID,
    session: DBSession,
    _: CurrentUser,
) -> ApiResponse[ArtifactRead]:
    artifact = await ArtifactService.get_artifact(session=session, artifact_id=artifact_id)
    return ApiResponse(message="Artifact fetched successfully", data=artifact)


@router.get(
    "/users/{user_id}/artifacts",
    response_model=ApiResponse[list[UserArtifactRead]],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def list_user_artifacts(
    user_id: UUID,
    session: DBSession,
    _: CurrentUser,
) -> ApiResponse[list[UserArtifactRead]]:
    artifacts = await ArtifactService.list_user_artifacts(session=session, user_id=user_id)
    return ApiResponse(message="User artifacts fetched successfully", data=artifacts)
