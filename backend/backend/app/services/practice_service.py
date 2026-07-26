from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.enums import EventType, PracticeStatus
from app.models.practice_challenge import PracticeChallenge
from app.models.user import User
from app.models.user_event import UserEvent
from app.schemas.practice import (
    PracticeChallengeRead,
    PracticeChallengeSummary,
    PracticeSolutionRead,
    PracticeSubmissionRequest,
    PracticeSubmissionResult,
    PracticeTestCaseResult,
)
from app.services.event_service import EventService
from app.services.service_utils import ensure_dict_list
from app.utils.code_execution import CodeExecutionService

PRACTICE_EXECUTION_TIMEOUT_SECONDS = 5


class PracticeService:
    """Handles practice retrieval, evaluation, and solution access workflows."""

    @staticmethod
    def normalize_output(output: str | None) -> str:
        """Normalizes Python output for deterministic test comparison."""
        if output is None:
            return ""
        normalized_lines = [line.rstrip() for line in output.replace("\r\n", "\n").strip().split("\n")]
        return "\n".join(normalized_lines).strip()

    @classmethod
    def outputs_match(cls, expected_output: str | None, actual_output: str | None) -> bool:
        """Compares expected and actual output using normalized values."""
        return cls.normalize_output(expected_output) == cls.normalize_output(actual_output)

    @classmethod
    def build_test_results(
        cls,
        *,
        test_cases: list[dict[str, Any]],
        actual_outputs: list[str | None],
    ) -> list[PracticeTestCaseResult]:
        """Builds per-test-case evaluation results for a submission."""
        results: list[PracticeTestCaseResult] = []
        for index, test_case in enumerate(test_cases):
            expected_output = test_case.get("expected_output")
            actual_output = actual_outputs[index] if index < len(actual_outputs) else None
            results.append(
                PracticeTestCaseResult(
                    name=test_case.get("name"),
                    input=test_case.get("input"),
                    expected_output=expected_output,
                    actual_output=actual_output,
                    passed=cls.outputs_match(str(expected_output or ""), str(actual_output or "")),
                )
            )
        return results

    @staticmethod
    def summarize_submission(*, practice_id: UUID, test_results: list[PracticeTestCaseResult], feedback: str) -> PracticeSubmissionResult:
        """Builds a normalized submission response from raw test results."""
        passed = all(result.passed for result in test_results) if test_results else False
        return PracticeSubmissionResult(
            practice_id=practice_id,
            passed=passed,
            xp_awarded=0,
            feedback=feedback,
            test_results=test_results,
            hints_used=0,
        )

    @staticmethod
    def serialize_practice(practice: PracticeChallenge) -> PracticeChallengeRead:
        """Serializes a practice challenge into a detailed response model."""
        test_cases = ensure_dict_list(practice.test_cases)
        hints = [str(item.get("text", item)) if isinstance(item, dict) else str(item) for item in (practice.hints or [])]
        return PracticeChallengeRead(
            id=practice.id,
            planet_id=practice.planet_id,
            title=practice.title,
            challenge_type=practice.challenge_type,
            difficulty=practice.difficulty,
            description=practice.description,
            learning_outcome=practice.learning_outcome,
            xp_reward=practice.xp_reward,
            solution_code=practice.solution_code,
            hints=hints,
            test_cases=test_cases,
            order_number=practice.order_number,
            status=practice.status,
            created_at=practice.created_at,
            updated_at=practice.updated_at,
        )

    @staticmethod
    def serialize_summary(
        practice: PracticeChallenge,
        status_override: PracticeStatus | str | None = None,
    ) -> PracticeChallengeSummary:
        """Serializes a practice challenge into a summary response model."""
        return PracticeChallengeSummary(
            id=practice.id,
            planet_id=practice.planet_id,
            title=practice.title,
            challenge_type=practice.challenge_type,
            difficulty=practice.difficulty,
            description=practice.description,
            learning_outcome=practice.learning_outcome,
            xp_reward=practice.xp_reward,
            order_number=practice.order_number,
            status=status_override or practice.status,
        )

    @staticmethod
    def build_feedback(test_results: list[PracticeTestCaseResult]) -> str:
        """Generates learner-facing feedback from practice test results."""
        if not test_results:
            return "No test cases were available for this challenge."
        if all(result.passed for result in test_results):
            return "Practice challenge completed successfully."
        failed_count = sum(1 for result in test_results if not result.passed)
        return f"Submission failed {failed_count} test case(s). Review the expected and actual outputs."

    @classmethod
    async def get_practice(cls, session: AsyncSession, practice_id: UUID) -> PracticeChallengeRead:
        """Returns a single practice challenge by identifier."""
        practice = await session.get(PracticeChallenge, practice_id)
        if practice is None:
            raise AppException(message="Practice challenge not found", status_code=404)
        return cls.serialize_practice(practice)

    @classmethod
    async def list_planet_practices(cls, session: AsyncSession, planet_id: UUID) -> list[PracticeChallengeSummary]:
        """Returns all practice challenges for a planet."""
        result = await session.execute(
            select(PracticeChallenge)
            .where(PracticeChallenge.planet_id == planet_id)
            .order_by(PracticeChallenge.order_number.asc())
        )
        return [cls.serialize_summary(practice) for practice in result.scalars().all()]

    @classmethod
    async def record_solution_view(cls, session: AsyncSession, *, user_id: UUID, practice_id: UUID) -> None:
        """Records that a learner viewed the reference solution."""
        await EventService.track_event(
            session=session,
            user_id=user_id,
            event_type=EventType.PRACTICE_SOLUTION_VIEWED,
            event_data={"practice_id": str(practice_id)},
        )
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    @classmethod
    async def get_solution(
        cls,
        session: AsyncSession,
        *,
        practice_id: UUID,
        user_id: UUID | None = None,
    ) -> PracticeSolutionRead:
        """Returns the reference solution and applies the viewed-solution side effect."""
        practice = await session.get(PracticeChallenge, practice_id)
        if practice is None:
            raise AppException(message="Practice challenge not found", status_code=404)
        if not practice.solution_code:
            raise AppException(message="Reference solution is not available", status_code=404)

        if user_id is not None:
            await cls.record_solution_view(session=session, user_id=user_id, practice_id=practice_id)

        return PracticeSolutionRead(
            practice_id=practice.id,
            solution_code=practice.solution_code,
            xp_if_claimed=practice.xp_reward // 2,
        )

    @staticmethod
    async def has_viewed_solution(session: AsyncSession, *, user_id: UUID, practice_id: UUID) -> bool:
        """Returns whether a learner has already viewed a practice solution."""
        result = await session.execute(
            select(UserEvent.id)
            .where(
                UserEvent.user_id == user_id,
                UserEvent.event_type == EventType.PRACTICE_SOLUTION_VIEWED,
                UserEvent.event_data["practice_id"].astext == str(practice_id),
            )
            .limit(1)
        )
        return result.scalar() is not None

    @classmethod
    async def submit_practice(
        cls,
        session: AsyncSession,
        *,
        user: User,
        practice_id: UUID,
        payload: PracticeSubmissionRequest,
    ) -> PracticeSubmissionResult:
        """Executes and evaluates a practice submission before progress orchestration."""
        practice = await session.get(PracticeChallenge, practice_id)
        if practice is None:
            raise AppException(message="Practice challenge not found", status_code=404)

        test_cases = ensure_dict_list(practice.test_cases)
        if not test_cases:
            raise AppException(message="Practice challenge does not have configured test cases", status_code=422)

        actual_outputs: list[str | None] = []
        for test_case in test_cases:
            execution = CodeExecutionService.execute_python_code(
                code=payload.submitted_code,
                stdin_input=str(test_case.get("input", "")),
                timeout_seconds=PRACTICE_EXECUTION_TIMEOUT_SECONDS,
            )
            if execution.timed_out:
                actual_outputs.append((execution.stdout or "") + "\nExecution timed out")
            elif execution.exit_code != 0:
                actual_outputs.append((execution.stdout or "") + (execution.stderr or ""))
            else:
                actual_outputs.append(execution.stdout)

        test_results = cls.build_test_results(test_cases=test_cases, actual_outputs=actual_outputs)
        summary = cls.summarize_submission(
            practice_id=practice.id,
            test_results=test_results,
            feedback=cls.build_feedback(test_results),
        )

        from app.services.progress_service import ProgressService

        used_solution = await cls.has_viewed_solution(session=session, user_id=user.id, practice_id=practice.id)
        return await ProgressService.complete_practice(
            session=session,
            user=user,
            practice=practice,
            submission_result=summary,
            used_solution=used_solution,
        )
