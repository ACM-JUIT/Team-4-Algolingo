from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.discovery import Discovery
from app.seeds.data.discoveries import DISCOVERIES, DiscoverySeedData
from app.seeds.utils import (
    SeedContext,
    SeedStats,
    add_all_and_flush,
    fetch_existing_by_composite,
    require_mapping_value,
)


class DiscoverySeeder:
    """Seeds discovery records into the database."""

    label = "Discoveries"

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    async def seed(self, session: AsyncSession, context: SeedContext) -> SeedStats:
        """Seeds discoveries using resolved planet references."""

        stats = SeedStats(label=self.label)
        discovery_records: tuple[DiscoverySeedData, ...] = DISCOVERIES
        if not discovery_records:
            return stats

        resolved_records: list[tuple[DiscoverySeedData, UUID]] = []
        composite_keys: list[tuple[UUID, int]] = []
        for record in discovery_records:
            planet_id = require_mapping_value(context.planet_ids, record["planet_key"], entity_label="planet")
            resolved_records.append((record, planet_id))
            composite_keys.append((planet_id, record["order_number"]))

        existing_by_key = await fetch_existing_by_composite(
            session=session,
            model=Discovery,
            columns=(Discovery.planet_id, Discovery.order_number),
            keys=composite_keys,
        )

        new_models: list[Discovery] = []
        pending_keys: list[str] = []
        for record, planet_id in resolved_records:
            composite_key = (planet_id, record["order_number"])
            existing = existing_by_key.get(composite_key)
            if existing is not None:
                context.discovery_ids[record["key"]] = existing.id
                stats.skipped += 1
                continue

            discovery = Discovery(
                planet_id=planet_id,
                title=record["title"],
                description=record["description"],
                content_md=record["content_md"],
                learning_objective=record["learning_objective"],
                read_time_minutes=record["read_time_minutes"],
                difficulty=record["difficulty"],
                xp_reward=record["xp_reward"],
                order_number=record["order_number"],
                status=record["status"],
                prerequisites=record["prerequisites"],
            )
            new_models.append(discovery)
            pending_keys.append(record["key"])

        await add_all_and_flush(session, new_models)
        for record_key, discovery in zip(pending_keys, new_models, strict=True):
            context.discovery_ids[record_key] = discovery.id
        stats.inserted = len(new_models)
        return stats
