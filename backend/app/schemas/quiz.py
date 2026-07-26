from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.artifact import ArtifactSummary
from app.schemas.base import ORMBaseSchema, UUIDReadSchema
from app.schemas.enums import QuizQuestionTypeEnum, QuizStatusEnum


class QuizQuestionOption(ORMBaseSchema):
    id: str
    text: str


class QuizQuestionRead(UUIDReadSchema):
    planet_id: UUID
    question_text: str
    question_type: QuizQuestionTypeEnum
    options: list[QuizQuestionOption] = Field(default_factory=list)
    explanation: str | None = None
    difficulty: int = Field(ge=1, le=5)
    xp_reward: int = Field(ge=0)
    order_number: int = Field(ge=1)


class QuizAnswerSubmission(ORMBaseSchema):
    question_id: UUID
    answer: str = Field(min_length=1, max_length=5000)


class QuizSubmitRequest(ORMBaseSchema):
    answers: list[QuizAnswerSubmission] = Field(min_length=1)


class QuizQuestionResult(ORMBaseSchema):
    question_id: UUID
    submitted_answer: str | None = None
    correct_answer: str
    is_correct: bool
    explanation: str | None = None


class QuizAttemptRead(ORMBaseSchema):
    id: UUID
    user_id: UUID
    planet_id: UUID
    score: int = Field(ge=0)
    total_questions: int = Field(ge=0)
    answers: list[dict[str, object]] = Field(default_factory=list)
    passed: bool
    xp_earned: int = Field(ge=0)
    attempted_at: datetime


class QuizOverview(ORMBaseSchema):
    planet_id: UUID
    total_questions: int = Field(ge=0)
    status: QuizStatusEnum
    best_score: int | None = Field(default=None, ge=0)
    attempts_count: int = Field(default=0, ge=0)
    passed: bool = False


class QuizSubmitResult(ORMBaseSchema):
    attempt_id: UUID | None = None
    score: int = Field(ge=0)
    total_questions: int = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
    passed: bool
    xp_awarded: int = Field(ge=0)
    quiz_status: QuizStatusEnum
    results: list[QuizQuestionResult] = Field(default_factory=list)
    artifact_unlocked: ArtifactSummary | None = None
