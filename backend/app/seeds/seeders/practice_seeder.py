from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.practice_challenge import PracticeChallenge
from app.seeds.data.practices import PRACTICES, PracticeSeedData
from app.seeds.utils import (
    SeedContext,
    SeedStats,
    add_all_and_flush,
    fetch_existing_by_composite,
    require_mapping_value,
)


class PracticeSeeder:
    """Seeds practice challenge records into the database."""

    label = "Practice Challenges"

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    async def seed(self, session: AsyncSession, context: SeedContext) -> SeedStats:
        """Seeds practice challenges using resolved planet references."""

        stats = SeedStats(label=self.label)
        practice_records: tuple[PracticeSeedData, ...] = PRACTICES
        if not practice_records:
            return stats

        resolved_records: list[tuple[PracticeSeedData, UUID]] = []
        composite_keys: list[tuple[UUID, int]] = []
        for record in practice_records:
            planet_id = require_mapping_value(context.planet_ids, record["planet_key"], entity_label="planet")
            resolved_records.append((record, planet_id))
            composite_keys.append((planet_id, record["order_number"]))

        existing_by_key = await fetch_existing_by_composite(
            session=session,
            model=PracticeChallenge,
            columns=(PracticeChallenge.planet_id, PracticeChallenge.order_number),
            keys=composite_keys,
        )

        new_models: list[PracticeChallenge] = []
        pending_keys: list[str] = []
        for record, planet_id in resolved_records:
            composite_key = (planet_id, record["order_number"])
            existing = existing_by_key.get(composite_key)
            if existing is not None:
                context.practice_ids[record["key"]] = existing.id
                stats.skipped += 1
                continue

            practice = PracticeChallenge(
                planet_id=planet_id,
                title=record["title"],
                challenge_type=record["challenge_type"],
                difficulty=record["difficulty"],
                description=record["description"],
                learning_outcome=record["learning_outcome"],
                xp_reward=record["xp_reward"],
                solution_code=record["solution_code"],
                hints=record["hints"],
                test_cases=record["test_cases"],
                order_number=record["order_number"],
                status=record["status"],
            )
            new_models.append(practice)
            pending_keys.append(record["key"])

        await add_all_and_flush(session, new_models)
        for record_key, practice in zip(pending_keys, new_models, strict=True):
            context.practice_ids[record_key] = practice.id
        stats.inserted = len(new_models)
        return stats
