from __future__ import annotations

from typing import TypedDict


class GalaxySeedData(TypedDict):
    key: str
    name: str
    description: str | None
    programming_language: str | None
    order_number: int
    is_locked: bool
    icon_url: str | None


GALAXIES: tuple[GalaxySeedData, ...] = (
    {
        "key": "python",
        "name": "Python",
        "description": (
            "Learn the foundations of programming with Python through short discoveries, guided practice, "
            "and knowledge-building quizzes."
        ),
        "programming_language": "Python",
        "order_number": 1,
        "is_locked": False,
        "icon_url": None,
    },
)
