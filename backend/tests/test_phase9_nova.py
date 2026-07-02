from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.models.nova_message import NovaMessage
from app.models.quiz_attempt import QuizAttempt
from app.models.user_progress import UserProgress
from app.schemas.event import UserEventRead
from app.services.context_builder import ContextBuilder
from app.services.prompt_builder import PromptBuilder


def test_prompt_builder_creates_title_and_system_prompt() -> None:
    title = PromptBuilder.build_session_title("   Explain Python variables and naming rules in detail   ")
    context = {
        "current_galaxy": {"name": "Python Nebula"},
        "current_planet": {"name": "Syntax Station"},
        "current_topic": "Variables",
        "user_level": 2,
        "user_rank": "Cadet",
        "user_xp": 500,
        "streak_days": 3,
    }

    system_prompt = PromptBuilder.build_system_prompt(mode="hint", context=context)

    assert title.startswith("Explain Python variables")
    assert "Python Nebula" in system_prompt
    assert "Syntax Station" in system_prompt
    assert "Hint generation" in system_prompt


def test_prompt_builder_builds_mode_specific_user_message() -> None:
    context = {
        "user_progress": {"completed_discoveries": ["d1"], "quiz_passed": False},
        "recent_quiz_performance": [{"score": 7, "total_questions": 10, "passed": True}],
        "recent_activity": ["discovery_completed"],
    }

    message = PromptBuilder.build_user_message(mode="debug", raw_message="My loop crashes", context=context)

    assert "debug this code" in message.lower()
    assert "recent quiz performance" in message.lower()
    assert "my loop crashes" in message.lower()


def test_context_builder_serializers() -> None:
    session_id = uuid4()
    history = ContextBuilder.serialize_history(
        [
            NovaMessage(
                id=uuid4(),
                session_id=session_id,
                sender="user",
                message="What is a variable?",
                context_data=None,
                created_at=datetime(2026, 6, 22, 0, 0, 0),
            ),
            NovaMessage(
                id=uuid4(),
                session_id=session_id,
                sender="assistant",
                message="A variable stores a value.",
                context_data=None,
                created_at=datetime(2026, 6, 22, 0, 0, 1),
            ),
        ]
    )
    events = [
        UserEventRead(
            id=uuid4(),
            user_id=uuid4(),
            event_type="discovery_completed",
            event_data=None,
            created_at=datetime(2026, 6, 22, 0, 0, 0),
        )
    ]
    attempts = [
        QuizAttempt(
            id=uuid4(),
            user_id=uuid4(),
            planet_id=uuid4(),
            score=7,
            total_questions=10,
            answers=[],
            passed=True,
            xp_earned=200,
            attempted_at=datetime(2026, 6, 22, 0, 0, 0),
        )
    ]
    progress = UserProgress(
        id=uuid4(),
        user_id=uuid4(),
        planet_id=uuid4(),
        completed_discoveries=["d1"],
        completed_practices=["p1"],
        quiz_passed=False,
        quiz_best_score=7,
        completed=False,
        status="IN_PROGRESS",
        xp_earned=250,
    )

    assert history[0]["role"] == "user"
    assert ContextBuilder.summarize_recent_activity(events) == ["discovery_completed"]
    assert ContextBuilder.summarize_quiz_performance(attempts)[0]["score"] == 7
    assert ContextBuilder.summarize_progress(progress)["completed_discoveries"] == ["d1"]
