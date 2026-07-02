from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.artifact import Artifact
from app.seeds.data.artifacts import ARTIFACTS, ArtifactSeedData
from app.seeds.utils import SeedContext, SeedStats, add_all_and_flush, fetch_existing_by_scalar


class ArtifactSeeder:
    """Seeds artifact records into the database."""

    label = "Artifacts"

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    async def seed(self, session: AsyncSession, context: SeedContext) -> SeedStats:
        """Seeds artifacts and stores stable key-to-ID mappings."""

        stats = SeedStats(label=self.label)
        artifact_records: tuple[ArtifactSeedData, ...] = ARTIFACTS
        if not artifact_records:
            return stats

        existing_by_name = await fetch_existing_by_scalar(
            session=session,
            model=Artifact,
            column=Artifact.name,
            values=(record["name"] for record in artifact_records),
        )

        new_models: list[Artifact] = []
        pending_keys: list[str] = []
        for record in artifact_records:
            existing = existing_by_name.get(record["name"])
            if existing is not None:
                context.artifact_ids[record["key"]] = existing.id
                stats.skipped += 1
                continue

            artifact = Artifact(
                name=record["name"],
                description=record["description"],
                rarity=record["rarity"],
                rarity_color=record["rarity_color"],
                category=record["category"],
                unlock_condition=record["unlock_condition"],
                xp_bonus_percent=record["xp_bonus_percent"],
                icon_url=record["icon_url"],
                display_order=record["display_order"],
                is_hidden=record["is_hidden"],
            )
            new_models.append(artifact)
            pending_keys.append(record["key"])

        await add_all_and_flush(session, new_models)
        for record_key, artifact in zip(pending_keys, new_models, strict=True):
            context.artifact_ids[record_key] = artifact.id
        stats.inserted = len(new_models)
        return stats
