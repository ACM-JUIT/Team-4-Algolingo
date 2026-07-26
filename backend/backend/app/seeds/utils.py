from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

ModelT = TypeVar("ModelT")

SEED_LOGGER_NAME = "app.seeds"


@dataclass(slots=True)
class SeedStats:
    """Tracks inserted and skipped rows for a seeding step."""

    label: str
    inserted: int = 0
    skipped: int = 0

    @property
    def processed(self) -> int:
        return self.inserted + self.skipped


@dataclass(slots=True)
class SeedContext:
    """Stores deterministic identifier maps produced during the seed run."""

    galaxy_ids: dict[str, UUID] = field(default_factory=dict)
    artifact_ids: dict[str, UUID] = field(default_factory=dict)
    planet_ids: dict[str, UUID] = field(default_factory=dict)
    discovery_ids: dict[str, UUID] = field(default_factory=dict)
    practice_ids: dict[str, UUID] = field(default_factory=dict)
    quiz_question_ids: dict[str, UUID] = field(default_factory=dict)


class SeedDataError(RuntimeError):
    """Raised when seed data references missing parent entities."""


class SeedExecutionError(RuntimeError):
    """Raised when the seed manager cannot complete a seed run."""



def get_seed_logger() -> logging.Logger:
    """Returns the shared logger used by the seed infrastructure."""

    return logging.getLogger(SEED_LOGGER_NAME)



def build_record_index(records: Sequence[dict[str, Any]], key_field: str = "key") -> dict[str, dict[str, Any]]:
    """Builds a key-indexed mapping for structured seed records."""

    return {str(record[key_field]): record for record in records}



def deduplicate_values(values: Iterable[Any]) -> list[Any]:
    """Returns ordered unique values while preserving input order."""

    return list(dict.fromkeys(values))



def require_mapping_value(mapping: dict[str, UUID], lookup_key: str | None, *, entity_label: str) -> UUID | None:
    """Resolves a key inside a seed context mapping or raises a seed data error."""

    if lookup_key is None:
        return None
    resolved_value = mapping.get(lookup_key)
    if resolved_value is None:
        raise SeedDataError(f"Missing {entity_label} reference: '{lookup_key}'.")
    return resolved_value


async def fetch_existing_by_scalar(
    session: AsyncSession,
    model: type[ModelT],
    column: InstrumentedAttribute[Any],
    values: Iterable[Any],
) -> dict[Any, ModelT]:
    """Fetches existing rows indexed by a single unique or lookup column."""

    unique_values = deduplicate_values(values)
    if not unique_values:
        return {}

    result = await session.execute(select(model).where(column.in_(unique_values)))
    items = result.scalars().all()
    return {getattr(item, column.key): item for item in items}


async def fetch_existing_by_composite(
    session: AsyncSession,
    model: type[ModelT],
    columns: Sequence[InstrumentedAttribute[Any]],
    keys: Iterable[tuple[Any, ...]],
) -> dict[tuple[Any, ...], ModelT]:
    """Fetches existing rows indexed by a composite unique key."""

    unique_keys = deduplicate_values(keys)
    if not unique_keys:
        return {}

    result = await session.execute(select(model).where(tuple_(*columns).in_(unique_keys)))
    items = result.scalars().all()
    return {
        tuple(getattr(item, column.key) for column in columns): item
        for item in items
    }


async def add_all_and_flush(session: AsyncSession, instances: Sequence[Any]) -> None:
    """Adds a batch of ORM instances and flushes them once."""

    if not instances:
        return
    session.add_all(list(instances))
    await session.flush()



def log_seed_start(logger: logging.Logger, label: str) -> None:
    """Logs the start of a seeding step."""

    logger.info("Seeding %s...", label)



def log_seed_result(logger: logging.Logger, stats: SeedStats) -> None:
    """Logs the result of a seeding step."""

    logger.info(
        "✓ %s inserted: %s | skipped: %s | processed: %s",
        stats.label,
        stats.inserted,
        stats.skipped,
        stats.processed,
    )
