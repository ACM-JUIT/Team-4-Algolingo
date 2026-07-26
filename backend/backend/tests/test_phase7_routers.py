from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pytest

from app.core.dependencies import get_current_active_user
from app.db.database import get_db_session
from app.main import app
from app.models.user import User
from app.schemas.artifact import ArtifactCollectionItem, ArtifactRead, ArtifactSummary, UserArtifactRead
from app.schemas.dashboard import DashboardQuickStats, DashboardRead
from app.schemas.discovery import DiscoveryRead
from app.schemas.enums import ArtifactCategoryEnum, ArtifactRarityEnum, LeaderboardTypeEnum, PlanetStatusEnum, RankTitleEnum
from app.schemas.galaxy import GalaxyDetail, GalaxyExplorerItem
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardRead, UserLeaderboardPosition
from app.schemas.nova import NovaMessageRead, NovaResponseData
from app.schemas.planet import PlanetDetail
from app.schemas.practice import PracticeChallengeRead, PracticeSolutionRead
from app.schemas.quiz import QuizQuestionRead, QuizQuestionResult, QuizSubmitResult
from app.schemas.user import UserProfileRead, UserProfileStats, UserPublicProfile, UserRead
from app.services.artifact_service import ArtifactService
from app.services.dashboard_service import DashboardService
from app.services.discovery_service import DiscoveryService
from app.services.galaxy_service import GalaxyService
from app.services.leaderboard_service import LeaderboardService
from app.services.nova_service import NovaService
from app.services.planet_service import PlanetService
from app.services.practice_service import PracticeService
from app.services.progress_service import ProgressService
from app.services.quiz_service import QuizService
from app.services.user_service import UserService


@pytest.fixture
def fake_current_user() -> User:
    return User(
        id=uuid4(),
        username="captain_one",
        email="captain@example.com",
        password_hash="hashed",
        xp=500,
        level=2,
        rank_title="Cadet",
        streak_days=1,
        status="ACTIVE",
        role="USER",
    )


@pytest.fixture(autouse=True)
def override_dependencies(fake_current_user: User):
    async def _override_current_user() -> User:
        return fake_current_user

    async def _override_db_session():
        yield object()

    app.dependency_overrides[get_current_active_user] = _override_current_user
    app.dependency_overrides[get_db_session] = _override_db_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_read(fake_current_user: User) -> UserRead:
    now = datetime(2026, 6, 22, 0, 0, 0)
    return UserRead(
        id=fake_current_user.id,
        username=fake_current_user.username,
        email=fake_current_user.email,
        avatar_url=None,
        bio=None,
        xp=500,
        level=2,
        rank_title="Cadet",
        streak_days=1,
        last_login_date=None,
        status="ACTIVE",
        role="USER",
        created_at=now,
        updated_at=now,
    )


def test_dashboard_route(client, monkeypatch, sample_user_read: UserRead):
    async def fake_get_dashboard(*args, **kwargs):
        return DashboardRead(
            user=sample_user_read,
            quick_stats=DashboardQuickStats(
                xp=500,
                level=2,
                rank_title=RankTitleEnum.CADET,
                streak_days=1,
                completed_planets=0,
                completed_discoveries=0,
                completed_practices=0,
                artifacts_earned=0,
            ),
            continue_learning=None,
            recent_activity=[],
            leaderboard_unlocked=False,
        )

    monkeypatch.setattr(DashboardService, "get_dashboard", fake_get_dashboard)
    response = client.get("/api/v1/dashboard")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["user"]["username"] == "captain_one"


def test_galaxies_routes(client, monkeypatch):
    galaxy_id = uuid4()
    now = datetime(2026, 6, 22, 0, 0, 0)

    async def fake_list_galaxies(*args, **kwargs):
        return [
            GalaxyExplorerItem(
                id=galaxy_id,
                name="Python Nebula",
                description="Learn Python",
                programming_language="Python",
                order_number=1,
                is_locked=False,
                icon_url=None,
                total_planets=3,
                completed_planets=1,
                progress_percent=33.33,
            )
        ]

    async def fake_get_galaxy_detail(*args, **kwargs):
        return GalaxyDetail(
            id=galaxy_id,
            name="Python Nebula",
            description="Learn Python",
            programming_language="Python",
            order_number=1,
            is_locked=False,
            icon_url=None,
            created_at=now,
            updated_at=now,
            planets=[],
        )

    monkeypatch.setattr(GalaxyService, "list_galaxies", fake_list_galaxies)
    monkeypatch.setattr(GalaxyService, "get_galaxy_detail", fake_get_galaxy_detail)

    list_response = client.get("/api/v1/galaxies")
    detail_response = client.get(f"/api/v1/galaxies/{galaxy_id}")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert list_response.json()["data"][0]["name"] == "Python Nebula"
    assert detail_response.json()["data"]["name"] == "Python Nebula"


def test_planet_route(client, monkeypatch):
    planet_id = uuid4()
    now = datetime(2026, 6, 22, 0, 0, 0)

    async def fake_get_planet_detail(*args, **kwargs):
        return PlanetDetail(
            id=planet_id,
            galaxy_id=uuid4(),
            artifact_id=None,
            name="Syntax Station",
            tagline="Start here",
            description="Basics",
            difficulty=1,
            order_number=1,
            xp_total=1150,
            estimated_time_minutes=90,
            status=PlanetStatusEnum.UNLOCKED,
            unlock_condition="Default",
            created_at=now,
            updated_at=now,
            discoveries=[],
            practice_challenges=[],
            quiz=None,
            artifact=None,
            progress=None,
        )

    monkeypatch.setattr(PlanetService, "get_planet_detail", fake_get_planet_detail)
    response = client.get(f"/api/v1/planets/{planet_id}")

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Syntax Station"


def test_users_profile_routes(client, monkeypatch, sample_user_read: UserRead):
    user_id = sample_user_read.id
    now = sample_user_read.created_at

    async def fake_get_public_profile(*args, **kwargs):
        return UserProfileRead(
            user=UserPublicProfile(
                id=user_id,
                username="captain_one",
                avatar_url=None,
                bio=None,
                xp=500,
                level=2,
                rank_title="Cadet",
                streak_days=1,
                created_at=now,
            ),
            stats=UserProfileStats(
                completed_planets=1,
                completed_discoveries=5,
                completed_practices=3,
                quizzes_passed=1,
                artifacts_earned=2,
            ),
        )

    async def fake_update_profile(*args, **kwargs):
        return sample_user_read

    monkeypatch.setattr(UserService, "get_public_profile", fake_get_public_profile)
    monkeypatch.setattr(UserService, "update_profile", fake_update_profile)

    get_response = client.get("/api/v1/profile/captain_one")
    patch_response = client.patch("/api/v1/profile/me", json={"bio": "Space learner"})

    assert get_response.status_code == 200
    assert patch_response.status_code == 200
    assert get_response.json()["data"]["user"]["username"] == "captain_one"
    assert patch_response.json()["data"]["email"] == "captain@example.com"


def test_discovery_routes(client, monkeypatch):
    discovery_id = uuid4()
    planet_id = uuid4()
    now = datetime(2026, 6, 22, 0, 0, 0)

    async def fake_get_discovery(*args, **kwargs):
        return DiscoveryRead(
            id=discovery_id,
            planet_id=planet_id,
            title="Your First Python Program",
            description="Intro",
            content_md="# Hello",
            learning_objective="Learn print",
            read_time_minutes=8,
            difficulty=1,
            xp_reward=75,
            order_number=1,
            status="AVAILABLE",
            prerequisites=[],
            created_at=now,
            updated_at=now,
        )

    async def fake_complete_discovery(*args, **kwargs):
        from app.schemas.discovery import DiscoveryCompletionResult
        return DiscoveryCompletionResult(
            discovery_id=discovery_id,
            planet_id=planet_id,
            completed=True,
            xp_awarded=75,
            total_completed_discoveries=1,
            planet_status=PlanetStatusEnum.IN_PROGRESS,
        )

    monkeypatch.setattr(DiscoveryService, "get_discovery", fake_get_discovery)
    monkeypatch.setattr(ProgressService, "complete_discovery", fake_complete_discovery)

    get_response = client.get(f"/api/v1/discoveries/{discovery_id}")
    complete_response = client.post(f"/api/v1/discoveries/{discovery_id}/complete")

    assert get_response.status_code == 200
    assert complete_response.status_code == 200
    assert get_response.json()["data"]["title"] == "Your First Python Program"
    assert complete_response.json()["data"]["xp_awarded"] == 75


def test_practice_routes(client, monkeypatch):
    practice_id = uuid4()
    now = datetime(2026, 6, 22, 0, 0, 0)

    async def fake_get_practice(*args, **kwargs):
        return PracticeChallengeRead(
            id=practice_id,
            planet_id=uuid4(),
            title="Welcome Aboard!",
            challenge_type="write_output",
            difficulty=1,
            description="Print hello",
            learning_outcome="Output basics",
            xp_reward=50,
            solution_code="print('Hello')",
            hints=["Use print"],
            test_cases=[],
            order_number=1,
            status="AVAILABLE",
            created_at=now,
            updated_at=now,
        )

    async def fake_get_solution(*args, **kwargs):
        return PracticeSolutionRead(
            practice_id=practice_id,
            solution_code="print('Hello')",
            xp_if_claimed=25,
        )

    async def fake_submit_practice(*args, **kwargs):
        from app.schemas.practice import PracticeSubmissionResult
        return PracticeSubmissionResult(
            practice_id=practice_id,
            passed=True,
            xp_awarded=50,
            feedback="Practice challenge completed successfully.",
            test_results=[],
            hints_used=0,
        )

    monkeypatch.setattr(PracticeService, "get_practice", fake_get_practice)
    monkeypatch.setattr(PracticeService, "get_solution", fake_get_solution)
    monkeypatch.setattr(PracticeService, "submit_practice", fake_submit_practice)

    get_response = client.get(f"/api/v1/practices/{practice_id}")
    solution_response = client.get(f"/api/v1/practices/{practice_id}/solution")
    submit_response = client.post(f"/api/v1/practices/{practice_id}/submit", json={"submitted_code": "print('Hello')"})

    assert get_response.status_code == 200
    assert solution_response.status_code == 200
    assert submit_response.status_code == 200
    assert solution_response.json()["data"]["xp_if_claimed"] == 25
    assert submit_response.json()["data"]["passed"] is True


def test_quiz_routes(client, monkeypatch):
    planet_id = uuid4()
    question_id = uuid4()

    async def fake_get_quiz_questions_for_user(*args, **kwargs):
        return [
            QuizQuestionRead(
                id=question_id,
                planet_id=planet_id,
                question_text="2 + 2?",
                question_type="multiple_choice",
                options=[],
                explanation="Basic math",
                difficulty=1,
                xp_reward=10,
                order_number=1,
            )
        ]

    async def fake_load_planet_with_quiz(*args, **kwargs):
        from app.models.planet import Planet
        from app.models.quiz_question import QuizQuestion
        return Planet(
            id=planet_id,
            galaxy_id=uuid4(),
            name="Syntax Station",
            difficulty=1,
            order_number=1,
            xp_total=100,
            quiz_questions=[
                QuizQuestion(
                    id=question_id,
                    planet_id=planet_id,
                    question_text="2 + 2?",
                    question_type="multiple_choice",
                    correct_answer="4",
                    difficulty=1,
                    xp_reward=10,
                    order_number=1,
                    explanation="Basic math",
                )
            ],
            discoveries=[],
            practice_challenges=[],
        )

    async def fake_submit_quiz(*args, **kwargs):
        return QuizSubmitResult(
            attempt_id=uuid4(),
            score=1,
            total_questions=1,
            percentage=100.0,
            passed=True,
            xp_awarded=10,
            quiz_status="PASSED",
            results=[
                QuizQuestionResult(
                    question_id=question_id,
                    submitted_answer="4",
                    correct_answer="4",
                    is_correct=True,
                    explanation="Basic math",
                )
            ],
            artifact_unlocked=None,
        )

    monkeypatch.setattr(QuizService, "get_quiz_questions_for_user", fake_get_quiz_questions_for_user)
    monkeypatch.setattr(QuizService, "load_planet_with_quiz", fake_load_planet_with_quiz)
    monkeypatch.setattr(ProgressService, "submit_quiz", fake_submit_quiz)

    get_planet_response = client.get(f"/api/v1/planets/{planet_id}/quiz")
    get_alias_response = client.get(f"/api/v1/quizzes/{planet_id}")
    submit_planet_response = client.post(
        f"/api/v1/planets/{planet_id}/quiz/submit",
        json={"answers": [{"question_id": str(question_id), "answer": "4"}]},
    )
    submit_alias_response = client.post(
        f"/api/v1/quizzes/{planet_id}/submit",
        json={"answers": [{"question_id": str(question_id), "answer": "4"}]},
    )

    assert get_planet_response.status_code == 200
    assert get_alias_response.status_code == 200
    assert submit_planet_response.status_code == 200
    assert submit_alias_response.status_code == 200
    assert get_planet_response.json()["data"][0]["question_text"] == "2 + 2?"
    assert get_alias_response.json()["data"][0]["question_text"] == "2 + 2?"
    assert submit_planet_response.json()["data"]["passed"] is True
    assert submit_alias_response.json()["data"]["passed"] is True


def test_artifact_routes(client, monkeypatch):
    artifact_id = uuid4()
    now = datetime(2026, 6, 22, 0, 0, 0)
    user_id = uuid4()

    async def fake_list_artifacts(*args, **kwargs):
        return [
            ArtifactCollectionItem(
                artifact=ArtifactRead(
                    id=artifact_id,
                    name="Syntax Sage",
                    description="Awarded for planet quiz",
                    rarity=ArtifactRarityEnum.COMMON,
                    rarity_color=None,
                    category=ArtifactCategoryEnum.PLANET,
                    unlock_condition="Pass Syntax Station quiz",
                    xp_bonus_percent=5,
                    icon_url=None,
                    display_order=1,
                    is_hidden=False,
                    created_at=now,
                    updated_at=now,
                ),
                collected=True,
                showcased=False,
                unlocked_at=now,
            )
        ]

    async def fake_get_artifact(*args, **kwargs):
        return ArtifactRead(
            id=artifact_id,
            name="Syntax Sage",
            description="Awarded for planet quiz",
            rarity=ArtifactRarityEnum.COMMON,
            rarity_color=None,
            category=ArtifactCategoryEnum.PLANET,
            unlock_condition="Pass Syntax Station quiz",
            xp_bonus_percent=5,
            icon_url=None,
            display_order=1,
            is_hidden=False,
            created_at=now,
            updated_at=now,
        )

    async def fake_list_user_artifacts(*args, **kwargs):
        return [
            UserArtifactRead(
                id=uuid4(),
                user_id=user_id,
                artifact_id=artifact_id,
                showcased=False,
                unlocked_at=now,
                artifact=ArtifactSummary(
                    id=artifact_id,
                    name="Syntax Sage",
                    rarity=ArtifactRarityEnum.COMMON,
                    category=ArtifactCategoryEnum.PLANET,
                    xp_bonus_percent=5,
                    icon_url=None,
                    is_hidden=False,
                ),
            )
        ]

    monkeypatch.setattr(ArtifactService, "list_artifacts", fake_list_artifacts)
    monkeypatch.setattr(ArtifactService, "get_artifact", fake_get_artifact)
    monkeypatch.setattr(ArtifactService, "list_user_artifacts", fake_list_user_artifacts)

    list_response = client.get("/api/v1/artifacts")
    detail_response = client.get(f"/api/v1/artifacts/{artifact_id}")
    user_response = client.get(f"/api/v1/users/{user_id}/artifacts")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert user_response.status_code == 200
    assert detail_response.json()["data"]["name"] == "Syntax Sage"


def test_leaderboard_route(client, monkeypatch):
    user_id = uuid4()

    async def fake_get_leaderboard(*args, **kwargs):
        return LeaderboardRead(
            leaderboard_type=LeaderboardTypeEnum.GLOBAL,
            items=[
                LeaderboardEntry(
                    position=1,
                    user_id=user_id,
                    username="captain_one",
                    avatar_url=None,
                    xp=1200,
                    level=3,
                    rank_title=RankTitleEnum.EXPLORER,
                )
            ],
            page=1,
            limit=20,
            total=1,
            snapshot_date=None,
            user_position=UserLeaderboardPosition(
                leaderboard_type=LeaderboardTypeEnum.GLOBAL,
                position=1,
                xp=1200,
            ),
        )

    monkeypatch.setattr(LeaderboardService, "get_leaderboard", fake_get_leaderboard)
    response = client.get("/api/v1/leaderboard?type=global&page=1&limit=20")

    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["position"] == 1


def test_nova_routes(client, monkeypatch):
    session_id = uuid4()
    now = datetime(2026, 6, 22, 0, 0, 0)

    async def fake_ask(*args, **kwargs):
        return NovaResponseData(
            session_id=session_id,
            reply="Captain, variables store values.",
            messages=[
                NovaMessageRead(
                    id=uuid4(),
                    session_id=session_id,
                    sender="assistant",
                    message="Captain, variables store values.",
                    context_data=None,
                    created_at=now,
                )
            ],
        )

    async def fake_hint(*args, **kwargs):
        return NovaResponseData(session_id=session_id, reply="Try using print first.", messages=[])

    async def fake_debug(*args, **kwargs):
        return NovaResponseData(session_id=session_id, reply="You missed a colon.", messages=[])

    async def fake_recommend(*args, **kwargs):
        return NovaResponseData(session_id=session_id, reply="Review control flow next.", messages=[])

    monkeypatch.setattr(NovaService, "ask", fake_ask)
    monkeypatch.setattr(NovaService, "hint", fake_hint)
    monkeypatch.setattr(NovaService, "debug", fake_debug)
    monkeypatch.setattr(NovaService, "recommend", fake_recommend)

    ask_response = client.post(
        "/api/v1/nova/ask",
        json={"message": "Explain variables", "session_id": None, "galaxy_id": None, "planet_id": None, "discovery_id": None, "practice_id": None},
    )
    hint_response = client.post(
        f"/api/v1/nova/hint/{uuid4()}",
        json={"current_code": "print('hi')", "specific_problem": "Need a hint", "session_id": None},
    )
    debug_response = client.post(
        "/api/v1/nova/debug",
        json={"code": "if True print('x')", "problem_description": "syntax error", "session_id": None, "galaxy_id": None, "planet_id": None, "practice_id": None},
    )
    recommend_response = client.post(
        "/api/v1/nova/recommend",
        json={"session_id": None, "galaxy_id": None, "planet_id": None},
    )

    assert ask_response.status_code == 200
    assert hint_response.status_code == 200
    assert debug_response.status_code == 200
    assert recommend_response.status_code == 200
    assert "variables" in ask_response.json()["data"]["reply"].lower()
