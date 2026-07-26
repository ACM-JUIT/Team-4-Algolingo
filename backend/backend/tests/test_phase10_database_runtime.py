from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.db import database as database_module


class FakeConnection:
    def __init__(self) -> None:
        self.executed = False

    async def execute(self, statement) -> None:
        self.executed = True
        self.statement = statement


class FakeConnectionManager:
    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection

    async def __aenter__(self) -> FakeConnection:
        return self.connection

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class FakeEngine:
    def __init__(self) -> None:
        self.connection = FakeConnection()
        self.disposed = False

    def connect(self) -> FakeConnectionManager:
        return FakeConnectionManager(self.connection)

    async def dispose(self) -> None:
        self.disposed = True


@pytest.mark.asyncio
async def test_ping_database_uses_engine_connection(monkeypatch) -> None:
    fake_engine = FakeEngine()
    monkeypatch.setattr(database_module, "engine", fake_engine)

    result = await database_module.ping_database()

    assert result is True
    assert fake_engine.connection.executed is True


@pytest.mark.asyncio
async def test_dispose_engine_calls_dispose(monkeypatch) -> None:
    fake_engine = FakeEngine()
    monkeypatch.setattr(database_module, "engine", fake_engine)

    await database_module.dispose_engine()

    assert fake_engine.disposed is True
