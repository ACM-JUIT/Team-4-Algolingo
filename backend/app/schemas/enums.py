from __future__ import annotations

from enum import StrEnum


class UserRoleEnum(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserStatusEnum(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"


class RankTitleEnum(StrEnum):
    CADET = "Cadet"
    EXPLORER = "Explorer"
    NAVIGATOR = "Navigator"
    COMMANDER = "Commander"
    GALACTIC_LEGEND = "Galactic Legend"


class PlanetStatusEnum(StrEnum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class DiscoveryStatusEnum(StrEnum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    COMPLETED = "COMPLETED"


class PracticeStatusEnum(StrEnum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    COMPLETED = "COMPLETED"


class QuizStatusEnum(StrEnum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    PASSED = "PASSED"
    FAILED = "FAILED"


class ArtifactRarityEnum(StrEnum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class ArtifactCategoryEnum(StrEnum):
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


class ChallengeTypeEnum(StrEnum):
    WRITE_OUTPUT = "write_output"
    FILL_BLANKS = "fill_blanks"
    CODE_WRITING = "code_writing"
    SCENARIO = "scenario"
    MCQ_CONCEPTUAL = "mcq_conceptual"
    ALGORITHM = "algorithm"


class QuizQuestionTypeEnum(StrEnum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    CODE_OUTPUT = "code_output"
    ERROR_DETECTION = "error_detection"


class LeaderboardTypeEnum(StrEnum):
    GLOBAL = "global"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    GALAXY = "galaxy"


class NovaSenderEnum(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    NOVA = "assistant"
    SYSTEM = "system"


class EventTypeEnum(StrEnum):
    DISCOVERY_COMPLETED = "discovery_completed"
    PRACTICE_COMPLETED = "practice_completed"
    QUIZ_PASSED = "quiz_passed"
    PLANET_COMPLETED = "planet_completed"
    ARTIFACT_UNLOCKED = "artifact_unlocked"
    DAILY_LOGIN = "daily_login"
    NOVA_USED = "nova_used"
    PRACTICE_SOLUTION_VIEWED = "practice_solution_viewed"
