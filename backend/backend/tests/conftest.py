from __future__ import annotations

import os
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.models  # noqa: F401
from app.core.dependencies import get_db_session
from app.db.base import Base
from app.main import app
from app.seeds.seed_manager import SeedManager
from app.seeds.utils import get_seed_logger


def _require_test_database_url() -> str:
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL is required to run integration tests.")
    return database_url


def _to_async_database_url(database_url: str) -> str:
    url = make_url(database_url)
    if "+asyncpg" in url.drivername:
        return url.render_as_string(hide_password=False)
    if url.drivername.startswith("postgresql"):
        return url.set(drivername="postgresql+asyncpg").render_as_string(hide_password=False)
    return database_url


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    database_url = _require_test_database_url()
    engine = create_async_engine(_to_async_database_url(database_url), pool_pre_ping=True)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def test_session_factory(test_engine):
    return async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


@pytest_asyncio.fixture(scope="session")
async def seeded_test_database(test_session_factory) -> None:
    async with test_session_factory() as session:
        manager = SeedManager(session=session, logger=get_seed_logger())
        await manager.run()


@pytest_asyncio.fixture
async def async_client(seeded_test_database, test_session_factory) -> AsyncGenerator[AsyncClient, None]:
    async def _override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = _override_get_db_session
    transport = ASGITransport(app=app, raise_app_exceptions=False)

    async with AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db_session, None)


@pytest_asyncio.fixture
async def db_session(test_session_factory) -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session
