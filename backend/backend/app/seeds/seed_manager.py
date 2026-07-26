from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.seeds.seeders import (
    ArtifactSeeder,
    DiscoverySeeder,
    GalaxySeeder,
    PlanetSeeder,
    PracticeSeeder,
    QuizSeeder,
)
from app.seeds.utils import (
    SeedContext,
    SeedExecutionError,
    SeedStats,
    log_seed_result,
    log_seed_start,
)


class SeedManager:
    """Coordinates seed execution order and transactional integrity."""

    def __init__(self, session: AsyncSession, logger: logging.Logger) -> None:
        self._session = session
        self._logger = logger
        self._context = SeedContext()
        self._seeders = (
            GalaxySeeder(logger),
            ArtifactSeeder(logger),
            PlanetSeeder(logger),
            DiscoverySeeder(logger),
            PracticeSeeder(logger),
            QuizSeeder(logger),
        )

    async def run(self) -> list[SeedStats]:
        """Executes all seeders in foreign-key-safe order within one transaction."""

        results: list[SeedStats] = []
        try:
            for seeder in self._seeders:
                log_seed_start(self._logger, seeder.label)
                stats = await seeder.seed(self._session, self._context)
                log_seed_result(self._logger, stats)
                results.append(stats)

            await self._session.commit()
        except Exception as exc:
            await self._session.rollback()
            raise SeedExecutionError("Seed process failed and the transaction was rolled back.") from exc

        self._logger.info("Finished successfully.")
        return results
