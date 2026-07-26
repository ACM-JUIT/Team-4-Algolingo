from app.routers.artifacts import router as artifacts_router
from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.discoveries import router as discoveries_router
from app.routers.galaxies import router as galaxies_router
from app.routers.leaderboard import router as leaderboard_router
from app.routers.nova import router as nova_router
from app.routers.planets import router as planets_router
from app.routers.practices import router as practices_router
from app.routers.quizzes import router as quizzes_router
from app.routers.users import router as users_router

__all__ = [
    "artifacts_router",
    "auth_router",
    "dashboard_router",
    "discoveries_router",
    "galaxies_router",
    "leaderboard_router",
    "nova_router",
    "planets_router",
    "practices_router",
    "quizzes_router",
    "users_router",
]
