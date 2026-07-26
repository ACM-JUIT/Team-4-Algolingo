from __future__ import annotations

import asyncio

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.database import AsyncSessionFactory, dispose_engine, ping_database
from app.seeds.seed_manager import SeedManager
from app.seeds.utils import get_seed_logger


async def seed_database() -> None:
    """Runs the full AlgoLingo database seed workflow."""

    settings = get_settings()
    setup_logging(settings)
    logger = get_seed_logger()

    logger.info("Initializing AlgoLingo database seed process...")
    try:
        await ping_database()
        async with AsyncSessionFactory() as session:
            manager = SeedManager(session=session, logger=logger)
            await manager.run()
    except Exception:
        logger.exception("Database seeding failed.")
        raise
    finally:
        await dispose_engine()


def main() -> None:
    """CLI entry point for running the AlgoLingo seed process."""

    asyncio.run(seed_database())


if __name__ == "__main__":
    main()
