from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.galaxy import Galaxy
from app.seeds.data.galaxies import GALAXIES, GalaxySeedData
from app.seeds.utils import SeedContext, SeedStats, add_all_and_flush, fetch_existing_by_scalar


class GalaxySeeder:
    """Seeds galaxy records into the database."""

    label = "Galaxies"

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    async def seed(self, session: AsyncSession, context: SeedContext) -> SeedStats:
        """Seeds galaxies and stores stable key-to-ID mappings."""

        stats = SeedStats(label=self.label)
        galaxy_records: tuple[GalaxySeedData, ...] = GALAXIES
        if not galaxy_records:
            return stats

        existing_by_name = await fetch_existing_by_scalar(
            session=session,
            model=Galaxy,
            column=Galaxy.name,
            values=(record["name"] for record in galaxy_records),
        )

        new_models: list[Galaxy] = []
        pending_keys: list[str] = []
        for record in galaxy_records:
            existing = existing_by_name.get(record["name"])
            if existing is not None:
                context.galaxy_ids[record["key"]] = existing.id
                stats.skipped += 1
                continue

            galaxy = Galaxy(
                name=record["name"],
                description=record["description"],
                programming_language=record["programming_language"],
                order_number=record["order_number"],
                is_locked=record["is_locked"],
                icon_url=record["icon_url"],
            )
            new_models.append(galaxy)
            pending_keys.append(record["key"])

        await add_all_and_flush(session, new_models)
        for record_key, galaxy in zip(pending_keys, new_models, strict=True):
            context.galaxy_ids[record_key] = galaxy.id
        stats.inserted = len(new_models)
        return stats
