from __future__ import annotations

import math
from dataclasses import dataclass

from app.services.service_utils import calculate_percentage


@dataclass(slots=True)
class LevelSnapshot:
    current_level: int
    current_level_xp_floor: int
    next_level: int | None
    next_level_xp_requirement: int | None
    progress_percentage: float


class LevelService:
    @staticmethod
    def xp_required_for_level(level: int) -> int:
        if level <= 1:
            return 0
        return (250 * level * level) - (250 * level)

    @classmethod
    def determine_level(cls, xp: int) -> int:
        if xp <= 0:
            return 1

        level = int((1 + math.sqrt(1 + (xp / 62.5))) // 2)
        while cls.xp_required_for_level(level + 1) <= xp:
            level += 1
        while level > 1 and cls.xp_required_for_level(level) > xp:
            level -= 1
        return max(level, 1)

    @classmethod
    def build_level_snapshot(cls, xp: int) -> LevelSnapshot:
        current_level = cls.determine_level(xp)
        current_floor = cls.xp_required_for_level(current_level)
        next_level = current_level + 1
        next_requirement = cls.xp_required_for_level(next_level)
        progress_percentage = calculate_percentage(xp - current_floor, next_requirement - current_floor)

        return LevelSnapshot(
            current_level=current_level,
            current_level_xp_floor=current_floor,
            next_level=next_level,
            next_level_xp_requirement=next_requirement,
            progress_percentage=progress_percentage,
        )
