from __future__ import annotations

from typing import TypedDict

from app.models.enums import PlanetStatus


class PlanetSeedData(TypedDict):
    key: str
    galaxy_key: str
    artifact_key: str | None
    name: str
    tagline: str | None
    description: str | None
    difficulty: int
    order_number: int
    xp_total: int
    estimated_time_minutes: int | None
    status: PlanetStatus
    unlock_condition: str | None


PLANETS: tuple[PlanetSeedData, ...] = (
    {
        "key": "python_variables",
        "galaxy_key": "python",
        "artifact_key": "artifact_variable_vanguard",
        "name": "Variables",
        "tagline": "Store information, name it clearly, and make your first Python programs feel alive.",
        "description": (
            "Variables teaches learners one of the most important ideas in programming: "
            "storing data with meaningful names. Students learn what variables are, how to create them, "
            "how Python handles types, and how to write readable beginner-friendly code."
        ),
        "difficulty": 1,
        "estimated_time_minutes": 90,
        "xp_total": 1180,
        "unlock_condition": "Available by default.",
        "order_number": 1,
        "status": PlanetStatus.UNLOCKED,
    },
    {
        "key": "python_data_types",
        "galaxy_key": "python",
        "artifact_key": "artifact_type_orb",
        "name": "Data Types",
        "tagline": "Every value has a type.",
        "description": (
            "Data Types teaches learners how Python classifies values and why that matters. "
            "Students explore numbers, text, truth values, collections, None, type inspection, "
            "type conversion, and the difference between mutable and immutable objects."
        ),
        "difficulty": 1,
        "estimated_time_minutes": 35,
        "xp_total": 120,
        "unlock_condition": "Complete Variables.",
        "order_number": 2,
        "status": PlanetStatus.LOCKED,
    },
    {
        "key": "python_operators",
        "galaxy_key": "python",
        "artifact_key": "artifact_operator_blade",
        "name": "Operators",
        "tagline": "Make Python perform calculations and comparisons.",
        "description": (
            "Operators teaches learners how to make Python compute, compare, combine conditions, and build meaningful expressions. "
            "Students move from arithmetic and assignment to comparison, logical, membership, identity, and operator precedence."
        ),
        "difficulty": 1,
        "estimated_time_minutes": 40,
        "xp_total": 140,
        "unlock_condition": "Complete Data Types.",
        "order_number": 3,
        "status": PlanetStatus.LOCKED,
    },
    {
        "key": "python_conditionals",
        "galaxy_key": "python",
        "artifact_key": "artifact_logic_compass",
        "name": "Conditionals",
        "tagline": "Teach your code to make intelligent decisions.",
        "description": (
            "Conditionals teaches learners how Python makes decisions using boolean expressions and branching logic. "
            "Students learn to control program flow with if, else, elif, nested conditions, logical operators, "
            "and concise conditional expressions while building readable and practical decision-making code."
        ),
        "difficulty": 2,
        "estimated_time_minutes": 45,
        "xp_total": 170,
        "unlock_condition": "Complete Operators.",
        "order_number": 4,
        "status": PlanetStatus.LOCKED,
    },
    {
        "key": "python_loops",
        "galaxy_key": "python",
        "artifact_key": "artifact_infinity_ring",
        "name": "Loops",
        "tagline": "Automate repetitive tasks with powerful loops.",
        "description": (
            "Loops teaches learners how to repeat actions efficiently instead of writing the same code again and again. "
            "Students learn when to use for loops and while loops, how range() works, how to control repetition with "
            "break and continue, how pass behaves, and how to write safe, readable looping logic."
        ),
        "difficulty": 2,
        "estimated_time_minutes": 50,
        "xp_total": 180,
        "unlock_condition": "Complete Conditionals.",
        "order_number": 5,
        "status": PlanetStatus.LOCKED,
    },
    {
        "key": "python_functions",
        "galaxy_key": "python",
        "artifact_key": "artifact_function_scroll",
        "name": "Functions",
        "tagline": "Write once. Reuse forever.",
        "description": (
            "Functions concludes the Python Galaxy by teaching learners how to organize code into reusable, modular building blocks. "
            "Students learn how to define and call functions, work with parameters and return values, manage scope, use default "
            "and keyword arguments, and write cleaner programs with docstrings and good design habits."
        ),
        "difficulty": 2,
        "estimated_time_minutes": 60,
        "xp_total": 220,
        "unlock_condition": "Complete Loops.",
        "order_number": 6,
        "status": PlanetStatus.LOCKED,
    },
)
