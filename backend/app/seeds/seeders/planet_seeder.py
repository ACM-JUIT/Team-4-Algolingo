from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.planet import Planet
from app.seeds.data.planets import PLANETS, PlanetSeedData
from app.seeds.utils import (
    SeedContext,
    SeedStats,
    add_all_and_flush,
    fetch_existing_by_composite,
    require_mapping_value,
)


class PlanetSeeder:
    """Seeds planet records into the database."""

    label = "Planets"

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    async def seed(self, session: AsyncSession, context: SeedContext) -> SeedStats:
        """Seeds planets using resolved galaxy and artifact references."""

        stats = SeedStats(label=self.label)
        planet_records: tuple[PlanetSeedData, ...] = PLANETS
        if not planet_records:
            return stats

        resolved_records: list[tuple[PlanetSeedData, UUID, UUID | None]] = []
        composite_keys: list[tuple[UUID, int]] = []
        for record in planet_records:
            galaxy_id = require_mapping_value(context.galaxy_ids, record["galaxy_key"], entity_label="galaxy")
            artifact_id = require_mapping_value(context.artifact_ids, record["artifact_key"], entity_label="artifact")
            resolved_records.append((record, galaxy_id, artifact_id))
            composite_keys.append((galaxy_id, record["order_number"]))

        existing_by_key = await fetch_existing_by_composite(
            session=session,
            model=Planet,
            columns=(Planet.galaxy_id, Planet.order_number),
            keys=composite_keys,
        )

        new_models: list[Planet] = []
        pending_keys: list[str] = []
        for record, galaxy_id, artifact_id in resolved_records:
            composite_key = (galaxy_id, record["order_number"])
            existing = existing_by_key.get(composite_key)
            if existing is not None:
                context.planet_ids[record["key"]] = existing.id
                stats.skipped += 1
                continue

            planet = Planet(
                galaxy_id=galaxy_id,
                artifact_id=artifact_id,
                name=record["name"],
                tagline=record["tagline"],
                description=record["description"],
                difficulty=record["difficulty"],
                order_number=record["order_number"],
                xp_total=record["xp_total"],
                estimated_time_minutes=record["estimated_time_minutes"],
                status=record["status"],
                unlock_condition=record["unlock_condition"],
            )
            new_models.append(planet)
            pending_keys.append(record["key"])

        await add_all_and_flush(session, new_models)
        for record_key, planet in zip(pending_keys, new_models, strict=True):
            context.planet_ids[record_key] = planet.id
        stats.inserted = len(new_models)
        return stats
