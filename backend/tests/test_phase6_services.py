from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.models.discovery import Discovery
from app.models.galaxy import Galaxy
from app.models.planet import Planet
from app.models.practice_challenge import PracticeChallenge
from app.models.quiz_question import QuizQuestion
from app.models.user_progress import UserProgress
from app.schemas.quiz import QuizAnswerSubmission
from app.services.dashboard_service import DashboardService
from app.services.event_service import EventService
from app.services.galaxy_service import GalaxyService
from app.services.planet_service import PlanetService
from app.services.practice_service import PracticeService
from app.services.quiz_service import QuizService
from app.services.user_service import UserService


def test_event_service_normalizes_scalar_event_data() -> None:
    payload = EventService.normalize_event_data("hello")

    assert payload == {"value": "hello"}


def test_user_service_build_profile_stats_counts_progress() -> None:
    progress_rows = [
        UserProgress(
            user_id=uuid4(),
            planet_id=uuid4(),
            completed_discoveries=["d1", "d2"],
            completed_practices=["p1"],
            quiz_passed=True,
            completed=True,
            xp_earned=250,
            status="COMPLETED",
        ),
        UserProgress(
            user_id=uuid4(),
            planet_id=uuid4(),
            completed_discoveries=["d3"],
            completed_practices=["p2", "p3"],
            quiz_passed=False,
            completed=False,
            xp_earned=175,
            status="IN_PROGRESS",
        ),
    ]

    stats = UserService.build_profile_stats(progress_rows=progress_rows, artifacts_count=3)

    assert stats.completed_planets == 1
    assert stats.completed_discoveries == 3
    assert stats.completed_practices == 3
    assert stats.quizzes_passed == 1
    assert stats.artifacts_earned == 3


def test_practice_service_normalizes_output_and_builds_results() -> None:
    test_results = PracticeService.build_test_results(
        test_cases=[
            {"name": "case-1", "input": "", "expected_output": "Hello World"},
            {"name": "case-2", "input": "", "expected_output": "42"},
        ],
        actual_outputs=["Hello World  \n", "41"],
    )

    assert test_results[0].passed is True
    assert test_results[1].passed is False

    summary = PracticeService.summarize_submission(
        practice_id=uuid4(),
        test_results=test_results,
        feedback="Keep going",
    )
    assert summary.passed is False
    assert summary.feedback == "Keep going"


def test_quiz_service_grades_submission() -> None:
    question_1 = QuizQuestion(
        id=uuid4(),
        planet_id=uuid4(),
        question_text="2 + 2?",
        question_type="multiple_choice",
        correct_answer="4",
        difficulty=1,
        xp_reward=10,
        order_number=1,
        explanation="Basic math",
    )
    question_2 = QuizQuestion(
        id=uuid4(),
        planet_id=question_1.planet_id,
        question_text="Python keyword?",
        question_type="fill_blank",
        correct_answer="if",
        difficulty=1,
        xp_reward=10,
        order_number=2,
        explanation="Conditional keyword",
    )

    result = QuizService.grade_submission(
        questions=[question_1, question_2],
        submitted_answers=[
            QuizAnswerSubmission(question_id=question_1.id, answer="4"),
            QuizAnswerSubmission(question_id=question_2.id, answer="else"),
        ],
    )

    assert result.score == 1
    assert result.total_questions == 2
    assert result.passed is False
    assert len(result.results) == 2


def test_planet_service_builds_progress_summary() -> None:
    planet = Planet(
        id=uuid4(),
        galaxy_id=uuid4(),
        name="Syntax Station",
        difficulty=1,
        order_number=1,
        xp_total=1150,
        discoveries=[
            Discovery(id=uuid4(), planet_id=uuid4(), title="D1", difficulty=1, xp_reward=75, order_number=1),
            Discovery(id=uuid4(), planet_id=uuid4(), title="D2", difficulty=1, xp_reward=75, order_number=2),
        ],
        practice_challenges=[
            PracticeChallenge(
                id=uuid4(),
                planet_id=uuid4(),
                title="P1",
                challenge_type="write_output",
                difficulty=1,
                xp_reward=50,
                order_number=1,
            )
        ],
        quiz_questions=[],
        status="UNLOCKED",
    )
    progress = UserProgress(
        user_id=uuid4(),
        planet_id=planet.id,
        completed_discoveries=[str(planet.discoveries[0].id)],
        completed_practices=[],
        quiz_passed=False,
        quiz_best_score=4,
        completed=False,
        xp_earned=75,
        status="IN_PROGRESS",
        started_at=datetime(2026, 6, 22, 0, 0, 0),
        last_activity_at=datetime(2026, 6, 22, 1, 0, 0),
    )

    summary = PlanetService.build_progress_summary(
        user_id=progress.user_id,
        planet=planet,
        progress=progress,
        attempts_count=1,
    )

    assert summary.completed_discoveries_count == 1
    assert summary.total_discoveries == 2
    assert summary.quiz_status == "LOCKED"
    assert summary.progress_percent == 25.0


def test_dashboard_service_chooses_first_incomplete_planet() -> None:
    galaxy = Galaxy(
        id=uuid4(),
        name="Python Nebula",
        order_number=1,
        is_locked=False,
        planets=[],
    )
    first_planet = Planet(
        id=uuid4(),
        galaxy_id=galaxy.id,
        name="Syntax Station",
        difficulty=1,
        order_number=1,
        xp_total=100,
        discoveries=[Discovery(id=uuid4(), planet_id=uuid4(), title="D1", difficulty=1, xp_reward=75, order_number=1)],
        practice_challenges=[],
        quiz_questions=[],
    )
    second_planet = Planet(
        id=uuid4(),
        galaxy_id=galaxy.id,
        name="Control Flow Crater",
        difficulty=2,
        order_number=2,
        xp_total=200,
        discoveries=[Discovery(id=uuid4(), planet_id=uuid4(), title="D2", difficulty=1, xp_reward=75, order_number=1)],
        practice_challenges=[],
        quiz_questions=[],
    )
    galaxy.planets = [first_planet, second_planet]

    progress_map = {
        first_planet.id: UserProgress(
            user_id=uuid4(),
            planet_id=first_planet.id,
            completed_discoveries=[str(first_planet.discoveries[0].id)],
            completed_practices=[],
            quiz_passed=False,
            completed=False,
            xp_earned=75,
            status="IN_PROGRESS",
        )
    }

    card = DashboardService.choose_continue_learning(galaxies=[galaxy], progress_map=progress_map)

    assert card is not None
    assert card.planet_id == first_planet.id
    assert card.next_discovery_id is None


def test_galaxy_service_and_quiz_service_percentage_helpers() -> None:
    assert GalaxyService.calculate_progress_percent(completed_planets=1, total_planets=3) == 33.33
    assert QuizService.determine_passing_score(10) == 7
    assert QuizService.determine_quiz_status(
        all_discoveries_completed=True,
        all_practices_completed=True,
        quiz_passed=False,
        attempts_count=0,
    ) == "AVAILABLE"
