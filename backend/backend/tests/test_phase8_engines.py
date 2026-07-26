from __future__ import annotations

from uuid import uuid4

import pytest

from app.models.discovery import Discovery
from app.models.planet import Planet
from app.models.practice_challenge import PracticeChallenge
from app.models.user_progress import UserProgress
from app.schemas.enums import DiscoveryStatusEnum, PlanetStatusEnum, PracticeStatusEnum, RankTitleEnum
from app.services.level_service import LevelService
from app.services.progress_service import ProgressService
from app.services.rank_service import RankService
from app.services.xp_service import XPService
from app.utils.code_execution import CodeExecutionService
from app.core.exceptions import AppException


def test_level_service_formula_and_snapshot() -> None:
    assert LevelService.xp_required_for_level(1) == 0
    assert LevelService.xp_required_for_level(2) == 500
    assert LevelService.xp_required_for_level(3) == 1500
    assert LevelService.determine_level(0) == 1
    assert LevelService.determine_level(1499) == 2
    assert LevelService.determine_level(1500) == 3

    snapshot = LevelService.build_level_snapshot(1750)
    assert snapshot.current_level == 3
    assert snapshot.next_level == 4
    assert snapshot.progress_percentage == 16.67


def test_rank_service_determines_expected_rank() -> None:
    assert RankService.determine_rank(level=1, completed_planet_orders=set()) == RankTitleEnum.CADET
    assert RankService.determine_rank(level=3, completed_planet_orders={1}) == RankTitleEnum.EXPLORER
    assert RankService.determine_rank(level=6, completed_planet_orders={1, 2}) == RankTitleEnum.NAVIGATOR
    assert RankService.determine_rank(level=9, completed_planet_orders={1, 2, 3}) == RankTitleEnum.COMMANDER
    assert (
        RankService.determine_rank(level=12, completed_planet_orders={1, 2, 3}, global_position=42)
        == RankTitleEnum.GALACTIC_LEGEND
    )


def test_xp_service_bonus_calculation() -> None:
    award = XPService.build_award_result(current_xp=100, base_xp=200, bonus_percent=10)

    assert award.base_xp == 200
    assert award.bonus_xp == 20
    assert award.total_xp == 220
    assert award.new_total_xp == 320
    assert award.new_level == 1


def test_progress_service_status_determination() -> None:
    discovery_1 = Discovery(id=uuid4(), planet_id=uuid4(), title="D1", difficulty=1, xp_reward=75, order_number=1)
    discovery_2 = Discovery(id=uuid4(), planet_id=discovery_1.planet_id, title="D2", difficulty=1, xp_reward=75, order_number=2)
    practice_1 = PracticeChallenge(
        id=uuid4(),
        planet_id=discovery_1.planet_id,
        title="P1",
        challenge_type="write_output",
        difficulty=1,
        xp_reward=50,
        order_number=1,
    )
    practice_2 = PracticeChallenge(
        id=uuid4(),
        planet_id=discovery_1.planet_id,
        title="P2",
        challenge_type="write_output",
        difficulty=1,
        xp_reward=50,
        order_number=2,
    )
    planet = Planet(
        id=uuid4(),
        galaxy_id=uuid4(),
        name="Syntax Station",
        difficulty=1,
        order_number=1,
        xp_total=100,
        discoveries=[discovery_1, discovery_2],
        practice_challenges=[practice_1, practice_2],
        quiz_questions=[],
    )

    discovery_status = ProgressService.determine_discovery_status(
        discovery=discovery_2,
        planet=planet,
        completed_discovery_ids={str(discovery_1.id)},
        planet_status=PlanetStatusEnum.UNLOCKED,
    )
    practice_status = ProgressService.determine_practice_status(
        practice=practice_2,
        planet=planet,
        completed_practice_ids=set(),
        planet_status=PlanetStatusEnum.UNLOCKED,
    )

    assert discovery_status == DiscoveryStatusEnum.AVAILABLE
    assert practice_status == PracticeStatusEnum.LOCKED


def test_planet_status_map_is_sequential() -> None:
    planet_1 = Planet(id=uuid4(), galaxy_id=uuid4(), name="P1", difficulty=1, order_number=1, xp_total=100)
    planet_2 = Planet(id=uuid4(), galaxy_id=planet_1.galaxy_id, name="P2", difficulty=1, order_number=2, xp_total=100)
    progress_map = {
        planet_1.id: UserProgress(
            user_id=uuid4(),
            planet_id=planet_1.id,
            completed_discoveries=[],
            completed_practices=[],
            quiz_passed=True,
            completed=True,
            xp_earned=100,
            status="COMPLETED",
        )
    }

    statuses = ProgressService.build_planet_status_map(
        planets=[planet_1, planet_2],
        progress_map=progress_map,
        galaxy_locked=False,
    )

    assert statuses[planet_1.id] == PlanetStatusEnum.COMPLETED
    assert statuses[planet_2.id] == PlanetStatusEnum.UNLOCKED


def test_code_execution_service_blocks_unsafe_imports() -> None:
    with pytest.raises(AppException):
        CodeExecutionService.validate_code_safety("import os\nprint('x')")
