from __future__ import annotations

from typing import NotRequired, TypedDict

from app.models.enums import ArtifactCategory, ArtifactRarity


class ArtifactSeedData(TypedDict):
    key: str
    name: str
    description: str | None
    rarity: ArtifactRarity
    rarity_color: str | None
    category: ArtifactCategory
    unlock_condition: str | None
    xp_bonus_percent: int
    icon_name: NotRequired[str | None]
    icon_url: str | None
    display_order: int
    is_hidden: bool


ARTIFACTS: tuple[ArtifactSeedData, ...] = (
    {
        "key": "artifact_variable_vanguard",
        "name": "Variable Vanguard",
        "description": (
            "Awarded to explorers who can confidently create, name, and use Python variables in simple programs."
        ),
        "rarity": ArtifactRarity.COMMON,
        "rarity_color": "#38BDF8",
        "icon_url": None,
        "xp_bonus_percent": 5,
        "unlock_condition": "Pass the Variables quiz.",
        "display_order": 1,
        "category": ArtifactCategory.PLANET,
        "is_hidden": False,
    },
    {
        "key": "artifact_type_orb",
        "name": "Type Orb",
        "description": (
            "A glowing orb awarded to explorers who can identify, inspect, and convert Python data types with confidence."
        ),
        "rarity": ArtifactRarity.COMMON,
        "rarity_color": "#60A5FA",
        "icon_url": None,
        "xp_bonus_percent": 5,
        "unlock_condition": "Pass the Data Types quiz.",
        "display_order": 2,
        "category": ArtifactCategory.PLANET,
        "is_hidden": False,
    },
    {
        "key": "artifact_operator_blade",
        "name": "Operator Blade",
        "description": (
            "A sharp symbolic blade awarded to explorers who can calculate, compare, and combine Python expressions with confidence."
        ),
        "rarity": ArtifactRarity.COMMON,
        "rarity_color": "#34D399",
        "icon_url": None,
        "xp_bonus_percent": 5,
        "unlock_condition": "Pass the Operators quiz.",
        "display_order": 3,
        "category": ArtifactCategory.PLANET,
        "is_hidden": False,
    },
    {
        "key": "artifact_logic_compass",
        "name": "Logic Compass",
        "description": (
            "A rare compass awarded to explorers who can guide Python through decisions with clear and accurate logic."
        ),
        "rarity": ArtifactRarity.RARE,
        "rarity_color": "#A855F7",
        "icon_url": None,
        "xp_bonus_percent": 10,
        "unlock_condition": "Pass the Conditionals quiz.",
        "display_order": 4,
        "category": ArtifactCategory.PLANET,
        "is_hidden": False,
    },
    {
        "key": "artifact_infinity_ring",
        "name": "Infinity Ring",
        "description": (
            "A rare ring awarded to explorers who can control repetition, stop loops wisely, and iterate with confidence."
        ),
        "rarity": ArtifactRarity.RARE,
        "rarity_color": "#8B5CF6",
        "icon_url": None,
        "xp_bonus_percent": 10,
        "unlock_condition": "Pass the Loops quiz.",
        "display_order": 5,
        "category": ArtifactCategory.PLANET,
        "is_hidden": False,
    },
    {
        "key": "artifact_function_scroll",
        "name": "Function Scroll",
        "description": (
            "An epic scroll awarded to explorers who can design reusable functions, pass arguments wisely, and structure Python programs like thoughtful problem solvers."
        ),
        "rarity": ArtifactRarity.EPIC,
        "rarity_color": "#F59E0B",
        "icon_url": None,
        "xp_bonus_percent": 15,
        "unlock_condition": "Pass the Functions quiz.",
        "display_order": 6,
        "category": ArtifactCategory.PLANET,
        "is_hidden": False,
    },
)
