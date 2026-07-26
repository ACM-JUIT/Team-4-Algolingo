from __future__ import annotations

from tests.helpers import (
    assert_error_response,
    assert_success_response,
    build_correct_quiz_answers,
    complete_discoveries,
    complete_practices,
    create_authenticated_user,
    fetch_planet_by_name,
    fetch_quiz_questions_for_planet,
)


async def test_get_planet_quiz_is_locked_before_prerequisites(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_get_locked")
    planet = await fetch_planet_by_name(db_session, "Variables")

    response = await async_client.get(f"/api/v1/planets/{planet.id}/quiz", headers=user_context["headers"])
    await assert_error_response(response, expected_status=403, expected_message_substring="locked")


async def test_get_planet_quiz_returns_questions_when_unlocked(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_get")
    planet = await fetch_planet_by_name(db_session, "Variables")

    await complete_discoveries(async_client, user_context["headers"], test_session_factory, planet_name="Variables")
    await complete_practices(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    response = await async_client.get(f"/api/v1/planets/{planet.id}/quiz", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert len(data) == 10
    assert all("correct_answer" not in question for question in data)


async def test_quiz_submission_is_locked_before_prerequisites(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_locked")
    planet = await fetch_planet_by_name(db_session, "Variables")
    questions = await fetch_quiz_questions_for_planet(db_session, planet.id)

    response = await async_client.post(
        f"/api/v1/planets/{planet.id}/quiz/submit",
        headers=user_context["headers"],
        json={"answers": build_correct_quiz_answers(questions)},
    )

    await assert_error_response(response, expected_status=403, expected_message_substring="locked")


async def test_get_quiz_alias_is_locked_before_prerequisites(async_client, db_session) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_alias_locked")
    planet = await fetch_planet_by_name(db_session, "Variables")

    response = await async_client.get(f"/api/v1/quizzes/{planet.id}", headers=user_context["headers"])
    await assert_error_response(response, expected_status=403, expected_message_substring="locked")


async def test_quiz_alias_returns_questions_when_unlocked(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_alias_get")
    planet = await fetch_planet_by_name(db_session, "Variables")

    await complete_discoveries(async_client, user_context["headers"], test_session_factory, planet_name="Variables")
    await complete_practices(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    response = await async_client.get(f"/api/v1/quizzes/{planet.id}", headers=user_context["headers"])
    data = await assert_success_response(response)

    assert len(data) == 10
    assert all("correct_answer" not in question for question in data)


async def test_quiz_submission_scores_and_unlocks_artifact(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_submit")
    planet = await fetch_planet_by_name(db_session, "Variables")

    await complete_discoveries(async_client, user_context["headers"], test_session_factory, planet_name="Variables")
    await complete_practices(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    questions = await fetch_quiz_questions_for_planet(db_session, planet.id)
    response = await async_client.post(
        f"/api/v1/planets/{planet.id}/quiz/submit",
        headers=user_context["headers"],
        json={"answers": build_correct_quiz_answers(questions)},
    )
    data = await assert_success_response(response)

    assert data["passed"] is True
    assert data["score"] == 10
    assert data["total_questions"] == 10
    assert data["xp_awarded"] > 0
    assert data["artifact_unlocked"] is not None
    assert data["artifact_unlocked"]["name"] == "Variable Vanguard"


async def test_quiz_submission_alias_scores_correct_answers(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_submit_alias")
    planet = await fetch_planet_by_name(db_session, "Variables")

    await complete_discoveries(async_client, user_context["headers"], test_session_factory, planet_name="Variables")
    await complete_practices(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    questions = await fetch_quiz_questions_for_planet(db_session, planet.id)
    response = await async_client.post(
        f"/api/v1/quizzes/{planet.id}/submit",
        headers=user_context["headers"],
        json={"answers": build_correct_quiz_answers(questions)},
    )
    data = await assert_success_response(response)

    assert data["passed"] is True
    assert data["score"] == 10
    assert data["total_questions"] == 10


async def test_quiz_submission_alias_with_wrong_answers_returns_failed_result(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_submit_wrong")
    planet = await fetch_planet_by_name(db_session, "Variables")

    await complete_discoveries(async_client, user_context["headers"], test_session_factory, planet_name="Variables")
    await complete_practices(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    questions = await fetch_quiz_questions_for_planet(db_session, planet.id)
    wrong_answers = [
        {
            "question_id": str(question.id),
            "answer": "WRONG_OPTION",
        }
        for question in questions
    ]
    response = await async_client.post(
        f"/api/v1/quizzes/{planet.id}/submit",
        headers=user_context["headers"],
        json={"answers": wrong_answers},
    )
    data = await assert_success_response(response)

    assert data["passed"] is False
    assert data["score"] == 0
    assert data["total_questions"] == 10


async def test_quiz_submission_alias_blocks_immediate_retake_after_pass(async_client, db_session, test_session_factory) -> None:
    user_context = await create_authenticated_user(async_client, prefix="quiz_retake_alias")
    planet = await fetch_planet_by_name(db_session, "Variables")

    await complete_discoveries(async_client, user_context["headers"], test_session_factory, planet_name="Variables")
    await complete_practices(async_client, user_context["headers"], test_session_factory, planet_name="Variables")

    questions = await fetch_quiz_questions_for_planet(db_session, planet.id)
    correct_answers = build_correct_quiz_answers(questions)

    first_response = await async_client.post(
        f"/api/v1/quizzes/{planet.id}/submit",
        headers=user_context["headers"],
        json={"answers": correct_answers},
    )
    await assert_success_response(first_response)

    second_response = await async_client.post(
        f"/api/v1/quizzes/{planet.id}/submit",
        headers=user_context["headers"],
        json={"answers": correct_answers},
    )
    await assert_error_response(second_response, expected_status=403, expected_message_substring="retaken")
