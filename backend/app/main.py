from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.core.logging import setup_logging
from app.db.database import dispose_engine
from app.routers import (
    artifacts_router,
    auth_router,
    dashboard_router,
    discoveries_router,
    galaxies_router,
    leaderboard_router,
    nova_router,
    planets_router,
    practices_router,
    quizzes_router,
    users_router,
)

settings = get_settings()
setup_logging(settings)
logger = logging.getLogger(__name__)

OPENAPI_TAGS_METADATA = [
    {"name": "auth", "description": "Authentication endpoints for registration, login, token refresh, and session management."},
    {"name": "users", "description": "User profile endpoints for public profile retrieval and self-service profile updates."},
    {"name": "dashboard", "description": "Dashboard endpoints that return personalized progress and recent activity."},
    {"name": "galaxies", "description": "Galaxy explorer endpoints for listing galaxies and viewing their planets."},
    {"name": "planets", "description": "Planet endpoints that return detailed learning content and progress state."},
    {"name": "discoveries", "description": "Discovery lesson endpoints for reading lesson content and recording completion."},
    {"name": "practices", "description": "Practice challenge endpoints for retrieval, submission, and reference solutions."},
    {"name": "quizzes", "description": "Quiz endpoints for question retrieval and quiz submission flows."},
    {"name": "artifacts", "description": "Artifact endpoints for collection browsing and earned artifact inventories."},
    {"name": "leaderboard", "description": "Leaderboard endpoints for global, periodic, and galaxy-specific rankings."},
    {"name": "nova", "description": "NOVA AI endpoints for questions, hints, debugging, and learning recommendations."},
    {"name": "health", "description": "Operational health endpoints for readiness and service status checks."},
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Logs application startup and shutdown while ensuring engine disposal."""
    logger.info("Starting AlgoLingo backend", extra={"environment": settings.environment})
    yield
    await dispose_engine()
    logger.info("Stopped AlgoLingo backend")


app = FastAPI(
    title=settings.project_name,
    summary=settings.project_summary,
    description=settings.project_description,
    version=settings.project_version,
    debug=settings.debug,
    contact={
        "name": settings.project_contact_name,
        **({"email": settings.project_contact_email} if settings.project_contact_email else {}),
        **({"url": settings.project_contact_url} if settings.project_contact_url else {}),
    },
    license_info={
        "name": settings.project_license_name,
        **({"url": settings.project_license_url} if settings.project_license_url else {}),
    },
    terms_of_service=settings.project_terms_of_service_url,
    openapi_tags=OPENAPI_TAGS_METADATA,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.allowed_hosts and settings.allowed_hosts != ["*"]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id
    started_at = time.perf_counter()

    response: Response = await call_next(request)

    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-MS"] = str(duration_ms)

    logger.info(
        "%s %s -> %s (%sms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        extra={"request_id": request_id},
    )
    return response


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    return response


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
    logger.warning(
        "Application error on %s %s: %s",
        request.method,
        request.url.path,
        exc.message,
        extra={"request_id": getattr(request.state, "request_id", None)},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
        },
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(
        "Validation error on %s %s",
        request.method,
        request.url.path,
        extra={"request_id": getattr(request.state, "request_id", None)},
    )
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": exc.errors(),
        },
    )


def _internal_error_response() -> JSONResponse:
    """Returns the standard internal server error response payload."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
        },
    )


@app.exception_handler(ExceptionGroup)
async def handle_exception_group(request: Request, exc: ExceptionGroup) -> JSONResponse:
    logger.exception(
        "Unhandled exception group on %s %s",
        request.method,
        request.url.path,
        extra={"request_id": getattr(request.state, "request_id", None)},
    )
    return _internal_error_response()


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled server error on %s %s",
        request.method,
        request.url.path,
        extra={"request_id": getattr(request.state, "request_id", None)},
    )
    return _internal_error_response()


app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(users_router, prefix=settings.api_v1_prefix)
app.include_router(dashboard_router, prefix=settings.api_v1_prefix)
app.include_router(galaxies_router, prefix=settings.api_v1_prefix)
app.include_router(planets_router, prefix=settings.api_v1_prefix)
app.include_router(discoveries_router, prefix=settings.api_v1_prefix)
app.include_router(practices_router, prefix=settings.api_v1_prefix)
app.include_router(quizzes_router, prefix=settings.api_v1_prefix)
app.include_router(artifacts_router, prefix=settings.api_v1_prefix)
app.include_router(leaderboard_router, prefix=settings.api_v1_prefix)
app.include_router(nova_router, prefix=settings.api_v1_prefix)


@app.get(
    "/",
    tags=["health"],
    status_code=status.HTTP_200_OK,
    summary="API Root",
    description="Returns a lightweight landing response for the AlgoLingo API.",
    response_description="Application landing metadata returned successfully.",
)
async def root() -> dict[str, str | None]:
    """Returns public, non-sensitive API metadata for clients and operators."""
    return {
        "name": settings.project_summary,
        "version": settings.project_version,
        "status": "running",
        "docs": "/docs" if settings.debug else None,
        "redoc": "/redoc" if settings.debug else None,
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["health"],
    status_code=status.HTTP_200_OK,
    summary="Service Health",
    description="Returns the public health status of the AlgoLingo API service.",
    response_description="Service health returned successfully.",
)
async def health_check() -> dict[str, str]:
    """Returns the top-level health status for the running application."""
    return {
        "status": "ok",
        "service": settings.project_name,
        "environment": settings.environment,
    }


@app.get(
    f"{settings.api_v1_prefix}/health",
    tags=["health"],
    status_code=status.HTTP_200_OK,
    summary="API Health",
    description="Returns the versioned API health status for integration checks.",
    response_description="Versioned API health returned successfully.",
)
async def api_health_check() -> dict[str, str]:
    """Returns the versioned health status for API-aware consumers."""
    return {
        "status": "ok",
        "service": settings.project_name,
        "environment": settings.environment,
    }
