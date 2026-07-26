from __future__ import annotations

from enum import StrEnum
from typing import Any, TypeAlias

from sqlalchemy import Enum as SQLEnum

JSONDict: TypeAlias = dict[str, Any]
JSONDictList: TypeAlias = list[JSONDict]
JSONStringList: TypeAlias = list[str]
JSONPayload: TypeAlias = JSONDict | JSONDictList


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"


class UserRole(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


class RankTitle(StrEnum):
    CADET = "Cadet"
    EXPLORER = "Explorer"
    NAVIGATOR = "Navigator"
    COMMANDER = "Commander"
    GALACTIC_LEGEND = "Galactic Legend"


class PlanetStatus(StrEnum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class DiscoveryStatus(StrEnum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    COMPLETED = "COMPLETED"


class PracticeStatus(StrEnum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    COMPLETED = "COMPLETED"


class ProgressStatus(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class QuestionType(StrEnum):
    MULTIPLE_CHOICE = "multiple_choice"
    MCQ = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    FILL_IN_BLANK = "fill_blank"
    CODE_OUTPUT = "code_output"
    ERROR_DETECTION = "error_detection"


class ChallengeType(StrEnum):
    WRITE_OUTPUT = "write_output"
    OUTPUT = "write_output"
    FILL_BLANKS = "fill_blanks"
    CODE_WRITING = "code_writing"
    CODING = "code_writing"
    SCENARIO = "scenario"
    DEBUGGING = "scenario"
    MCQ_CONCEPTUAL = "mcq_conceptual"
    MCQ = "mcq_conceptual"
    ALGORITHM = "algorithm"


class ArtifactRarity(StrEnum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class ArtifactCategory(StrEnum):
    PLANET = "planet"
    GALAXY = "galaxy"
    MILESTONE = "milestone"
    STREAK = "streak"
    QUIZ = "quiz"
    COMPLETION = "completion"
    LEADERBOARD = "leaderboard"
    NOVA = "nova"
    HIDDEN = "hidden"
    SPECIAL = "special"
    ACHIEVEMENT = "achievement"


class LeaderboardType(StrEnum):
    GLOBAL = "global"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    GALAXY = "galaxy"


class NovaSender(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    NOVA = "assistant"
    SYSTEM = "system"


class EventType(StrEnum):
    DISCOVERY_COMPLETED = "discovery_completed"
    PRACTICE_COMPLETED = "practice_completed"
    QUIZ_PASSED = "quiz_passed"
    PLANET_COMPLETED = "planet_completed"
    ARTIFACT_UNLOCKED = "artifact_unlocked"
    DAILY_LOGIN = "daily_login"
    NOVA_USED = "nova_used"
    PRACTICE_SOLUTION_VIEWED = "practice_solution_viewed"


def build_sa_enum(enum_class: type[StrEnum], *, name: str, length: int) -> SQLEnum:
    """Build a SQLAlchemy enum that remains PostgreSQL- and Alembic-friendly."""

    return SQLEnum(
        enum_class,
        name=name,
        native_enum=False,
        validate_strings=True,
        create_constraint=False,
        values_callable=lambda enum_type: [member.value for member in enum_type],
        length=length,
    )


__all__ = [
    "ArtifactCategory",
    "ArtifactRarity",
    "ChallengeType",
    "DiscoveryStatus",
    "EventType",
    "JSONDict",
    "JSONDictList",
    "JSONPayload",
    "JSONStringList",
    "LeaderboardType",
    "NovaSender",
    "PlanetStatus",
    "PracticeStatus",
    "ProgressStatus",
    "QuestionType",
    "RankTitle",
    "UserRole",
    "UserStatus",
    "build_sa_enum",
]
