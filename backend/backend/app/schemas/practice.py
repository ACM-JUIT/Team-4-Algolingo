from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.base import ORMBaseSchema, UUIDTimestampedReadSchema
from app.schemas.enums import ChallengeTypeEnum, PracticeStatusEnum


class PracticeChallengeSummary(ORMBaseSchema):
    id: UUID
    planet_id: UUID
    title: str
    challenge_type: ChallengeTypeEnum
    difficulty: int = Field(ge=1, le=5)
    description: str | None = None
    learning_outcome: str | None = None
    xp_reward: int = Field(ge=0)
    order_number: int = Field(ge=1)
    status: PracticeStatusEnum


class PracticeChallengeRead(UUIDTimestampedReadSchema):
    planet_id: UUID
    title: str
    challenge_type: ChallengeTypeEnum
    difficulty: int = Field(ge=1, le=5)
    description: str | None = None
    learning_outcome: str | None = None
    xp_reward: int = Field(ge=0)
    solution_code: str | None = None
    hints: list[str] = Field(default_factory=list)
    test_cases: list[dict[str, object]] = Field(default_factory=list)
    order_number: int = Field(ge=1)
    status: PracticeStatusEnum


class PracticeSubmissionRequest(ORMBaseSchema):
    submitted_code: str = Field(min_length=1, max_length=20000)


class PracticeTestCaseResult(ORMBaseSchema):
    name: str | None = None
    input: str | None = None
    expected_output: str | None = None
    actual_output: str | None = None
    passed: bool


class PracticeSubmissionResult(ORMBaseSchema):
    practice_id: UUID
    passed: bool
    xp_awarded: int = Field(ge=0)
    feedback: str
    test_results: list[PracticeTestCaseResult] = Field(default_factory=list)
    hints_used: int = Field(default=0, ge=0)


class PracticeSolutionRead(ORMBaseSchema):
    practice_id: UUID
    solution_code: str
    xp_if_claimed: int = Field(ge=0)
