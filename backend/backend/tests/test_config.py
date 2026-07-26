from __future__ import annotations

from app.core.config import Settings


def test_settings_build_async_database_url() -> None:
    settings = Settings(
        _env_file=None,
        postgres_user="postgres",
        postgres_password="postgres",
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="algolingo",
    )

    assert settings.async_database_url == "postgresql+asyncpg://postgres:postgres@localhost:5432/algolingo"


def test_settings_build_sync_database_url() -> None:
    settings = Settings(
        _env_file=None,
        database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/algolingo",
    )

    assert settings.sync_database_url == "postgresql+psycopg://postgres:postgres@localhost:5432/algolingo"


def test_settings_parse_cors_origins() -> None:
    settings = Settings(
        _env_file=None,
        cors_origins="http://localhost:3000,http://127.0.0.1:5173",
    )

    assert settings.cors_origins == ["http://localhost:3000", "http://127.0.0.1:5173"]
