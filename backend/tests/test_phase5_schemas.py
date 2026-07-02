from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.artifact import ArtifactSummary
from app.schemas.enums import ArtifactCategoryEnum, ArtifactRarityEnum, LeaderboardTypeEnum, QuizStatusEnum
from app.schemas.galaxy import GalaxyDetail
from app.schemas.leaderboard import LeaderboardQueryParams
from app.schemas.nova import NovaAskRequest
from app.schemas.planet import PlanetDetail, PlanetProgressSummary
from app.schemas.practice import PracticeChallengeSummary, PracticeSubmissionRequest
from app.schemas.quiz import QuizOverview
from app.schemas.discovery import DiscoverySummary


def test_planet_detail_accepts_nested_payload() -> None:
    planet_id = uuid4()
    galaxy_id = uuid4()
    artifact_id = uuid4()

    payload = PlanetDetail(
        id=planet_id,
        galaxy_id=galaxy_id,
        artifact_id=artifact_id,
        name="Syntax Station",
        tagline="Master Python basics",
        description="Planet 1",
        difficulty=1,
        order_number=1,
        xp_total=1150,
        estimated_time_minutes=90,
        status="UNLOCKED",
        unlock_condition="Default",
        created_at="2026-06-22T00:00:00",
        updated_at="2026-06-22T00:00:00",
        discoveries=[
            DiscoverySummary(
                id=uuid4(),
                planet_id=planet_id,
                title="Your First Python Program",
                description="Intro",
                learning_objective="Learn print",
                read_time_minutes=8,
                difficulty=1,
                xp_reward=75,
                order_number=1,
                status="AVAILABLE",
                prerequisites=[],
            )
        ],
        practice_challenges=[
            PracticeChallengeSummary(
                id=uuid4(),
                planet_id=planet_id,
                title="Welcome Aboard!",
                challenge_type="write_output",
                difficulty=1,
                description="Write hello world",
                learning_outcome="Output text",
                xp_reward=50,
                order_number=1,
                status="AVAILABLE",
            )
        ],
        quiz=QuizOverview(
            planet_id=planet_id,
            total_questions=10,
            status=QuizStatusEnum.LOCKED,
            best_score=None,
            attempts_count=0,
            passed=False,
        ),
        artifact=ArtifactSummary(
            id=artifact_id,
            name="Syntax Sage",
            rarity=ArtifactRarityEnum.COMMON,
            category=ArtifactCategoryEnum.PLANET,
            xp_bonus_percent=5,
            icon_url=None,
            is_hidden=False,
        ),
        progress=PlanetProgressSummary(
            user_id=uuid4(),
            planet_id=planet_id,
            status="IN_PROGRESS",
            completed_discoveries_count=1,
            total_discoveries=7,
            completed_practices_count=0,
            total_practices=5,
            quiz_status="LOCKED",
            quiz_best_score=None,
            completed=False,
            xp_earned=75,
            started_at="2026-06-22T00:00:00",
            completed_at=None,
            last_activity_at="2026-06-22T00:00:00",
            progress_percent=10.0,
        ),
    )

    assert payload.name == "Syntax Station"
    assert payload.quiz is not None
    assert payload.quiz.status == QuizStatusEnum.LOCKED
    assert len(payload.discoveries) == 1


def test_galaxy_detail_accepts_nested_planets() -> None:
    payload = GalaxyDetail(
        id=uuid4(),
        name="Python Nebula",
        description="Learn Python",
        programming_language="Python",
        order_number=1,
        is_locked=False,
        icon_url=None,
        created_at="2026-06-22T00:00:00",
        updated_at="2026-06-22T00:00:00",
        planets=[],
    )

    assert payload.name == "Python Nebula"


def test_practice_submission_request_rejects_empty_code() -> None:
    with pytest.raises(ValidationError):
        PracticeSubmissionRequest(submitted_code="")


def test_leaderboard_query_params_limit_is_capped() -> None:
    with pytest.raises(ValidationError):
        LeaderboardQueryParams(type=LeaderboardTypeEnum.GLOBAL, page=1, limit=51)


def test_nova_ask_request_requires_message() -> None:
    with pytest.raises(ValidationError):
        NovaAskRequest(message="")
