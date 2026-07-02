from __future__ import annotations

import math
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AppException
from app.models.planet import Planet
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_question import QuizQuestion
from app.models.user import User
from app.models.user_progress import UserProgress
from app.schemas.enums import QuizStatusEnum
from app.schemas.quiz import (
    QuizAnswerSubmission,
    QuizOverview,
    QuizQuestionOption,
    QuizQuestionRead,
    QuizQuestionResult,
    QuizSubmitResult,
)
from app.services.service_utils import calculate_percentage, ensure_dict_list, ensure_string_list


class QuizService:
    @staticmethod
    def _sort_questions(questions: list[QuizQuestion]) -> list[QuizQuestion]:
        return sorted(questions, key=lambda question: question.order_number)

    @staticmethod
    def determine_passing_score(total_questions: int) -> int:
        if total_questions <= 0:
            return 0
        return math.ceil(total_questions * 0.7)

    @staticmethod
    def determine_quiz_status(
        *,
        all_discoveries_completed: bool,
        all_practices_completed: bool,
        quiz_passed: bool,
        attempts_count: int,
    ) -> QuizStatusEnum:
        if not (all_discoveries_completed and all_practices_completed):
            return QuizStatusEnum.LOCKED
        if quiz_passed:
            return QuizStatusEnum.PASSED
        if attempts_count > 0:
            return QuizStatusEnum.FAILED
        return QuizStatusEnum.AVAILABLE

    @staticmethod
    def grade_submission(
        *,
        questions: list[QuizQuestion],
        submitted_answers: list[QuizAnswerSubmission],
    ) -> QuizSubmitResult:
        answers_by_question_id = {str(answer.question_id): answer.answer for answer in submitted_answers}
        results: list[QuizQuestionResult] = []
        score = 0

        for question in questions:
            submitted_answer = answers_by_question_id.get(str(question.id))
            is_correct = (submitted_answer or "").strip() == question.correct_answer.strip()
            if is_correct:
                score += 1

            results.append(
                QuizQuestionResult(
                    question_id=question.id,
                    submitted_answer=submitted_answer,
                    correct_answer=question.correct_answer,
                    is_correct=is_correct,
                    explanation=question.explanation,
                )
            )

        total_questions = len(questions)
        passing_score = QuizService.determine_passing_score(total_questions)
        passed = score >= passing_score
        percentage = calculate_percentage(score, total_questions)

        return QuizSubmitResult(
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            xp_awarded=0,
            quiz_status=QuizStatusEnum.PASSED if passed else QuizStatusEnum.FAILED,
            results=results,
            artifact_unlocked=None,
        )

    @staticmethod
    def _serialize_options(question: QuizQuestion) -> list[QuizQuestionOption]:
        option_dicts = ensure_dict_list(question.options)
        return [QuizQuestionOption(id=str(item.get("id", "")), text=str(item.get("text", ""))) for item in option_dicts]

    @classmethod
    async def get_quiz_questions(cls, session: AsyncSession, planet_id: UUID) -> list[QuizQuestionRead]:
        result = await session.execute(
            select(QuizQuestion)
            .where(QuizQuestion.planet_id == planet_id)
            .order_by(QuizQuestion.order_number.asc())
        )
        questions = result.scalars().all()
        if not questions:
            raise AppException(message="Quiz questions not found for planet", status_code=404)

        return [
            QuizQuestionRead(
                id=question.id,
                planet_id=question.planet_id,
                question_text=question.question_text,
                question_type=question.question_type,
                options=cls._serialize_options(question),
                explanation=question.explanation,
                difficulty=question.difficulty,
                xp_reward=question.xp_reward,
                order_number=question.order_number,
            )
            for question in cls._sort_questions(questions)
        ]

    @classmethod
    async def get_quiz_overview(
        cls,
        session: AsyncSession,
        *,
        planet: Planet,
        user_id: UUID | None,
        progress: UserProgress | None = None,
    ) -> QuizOverview:
        attempts_count = 0
        if user_id is not None:
            attempts_count_result = await session.execute(
                select(func.count(QuizAttempt.id)).where(
                    QuizAttempt.user_id == user_id,
                    QuizAttempt.planet_id == planet.id,
                )
            )
            attempts_count = int(attempts_count_result.scalar_one() or 0)

        completed_discoveries_count = len(ensure_string_list(progress.completed_discoveries)) if progress else 0
        completed_practices_count = len(ensure_string_list(progress.completed_practices)) if progress else 0
        total_discoveries = len(planet.discoveries)
        total_practices = len(planet.practice_challenges)
        quiz_passed = bool(progress.quiz_passed) if progress else False

        status = cls.determine_quiz_status(
            all_discoveries_completed=completed_discoveries_count >= total_discoveries and total_discoveries > 0,
            all_practices_completed=completed_practices_count >= total_practices and total_practices > 0,
            quiz_passed=quiz_passed,
            attempts_count=attempts_count,
        )

        return QuizOverview(
            planet_id=planet.id,
            total_questions=len(planet.quiz_questions),
            status=status,
            best_score=progress.quiz_best_score if progress else None,
            attempts_count=attempts_count,
            passed=quiz_passed,
        )

    @classmethod
    async def load_planet_with_quiz(cls, session: AsyncSession, planet_id: UUID) -> Planet:
        result = await session.execute(
            select(Planet)
            .options(
                selectinload(Planet.discoveries),
                selectinload(Planet.practice_challenges),
                selectinload(Planet.quiz_questions),
                selectinload(Planet.galaxy),
                selectinload(Planet.artifact),
            )
            .where(Planet.id == planet_id)
        )
        planet = result.scalar_one_or_none()
        if planet is None:
            raise AppException(message="Planet not found", status_code=404)
        return planet

    @classmethod
    async def submit_quiz(
        cls,
        session: AsyncSession,
        *,
        user: User,
        planet_id: UUID,
        submitted_answers: list[QuizAnswerSubmission],
    ) -> QuizSubmitResult:
        """Loads, grades, and finalizes a quiz submission for a planet."""
        planet = await cls.load_planet_with_quiz(session=session, planet_id=planet_id)
        sorted_questions = cls._sort_questions(list(planet.quiz_questions))
        grading_result = cls.grade_submission(
            questions=sorted_questions,
            submitted_answers=submitted_answers,
        )

        from app.services.progress_service import ProgressService

        return await ProgressService.submit_quiz(
            session=session,
            user=user,
            planet_id=planet_id,
            questions=sorted_questions,
            grading_result=grading_result,
        )
