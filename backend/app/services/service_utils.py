from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any


def calculate_percentage(completed: int, total: int) -> float:
    if total <= 0:
        return 0.0

    percentage = (Decimal(completed) / Decimal(total)) * Decimal("100")
    return float(percentage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))



def ensure_string_list(value: Any) -> list[str]:
    if not value:
        return []

    result: list[str] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict) and "id" in item:
                result.append(str(item["id"]))
            else:
                result.append(str(item))
    return result



def ensure_dict_list(value: Any) -> list[dict[str, Any]]:
    if not value:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []
