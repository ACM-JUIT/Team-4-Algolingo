from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import AnyHttpUrl, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    project_name: str = "AlgoLingo Backend"
    project_version: str = "0.1.0"
    project_summary: str = "AlgoLingo API"
    project_description: str = (
        "AlgoLingo is a gamified programming learning platform powered by FastAPI, PostgreSQL, "
        "SQLAlchemy, and NOVA AI."
    )
    project_contact_name: str = "AlgoLingo Team"
    project_contact_email: str = "support@algolingo.dev"
    project_contact_url: str | None = None
    project_license_name: str = "Proprietary"
    project_license_url: str | None = None
    project_terms_of_service_url: str | None = None
    api_v1_prefix: str = "/api/v1"

    environment: Literal["development", "testing", "staging", "production"] = "development"
    debug: bool = True

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "algolingo"
    database_url: str | None = None

    sql_echo: bool = False
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    jwt_secret_key: str = "change-this-before-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    refresh_token_expire_days: int = 30

    ollama_base_url: AnyHttpUrl = "http://localhost:11434"
    ollama_model: str = "mistral:7b"
    ollama_timeout_seconds: float = 10.0
    nova_max_requests_per_hour: int = 30
    nova_max_response_tokens: int = 512
    nova_max_history_messages: int = 10

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    allowed_hosts: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        enable_decoding=False,
    )

    @field_validator("cors_origins", "allowed_hosts", mode="before")
    @classmethod
    def parse_str_list(cls, value: Any) -> list[str] | Any:
        if isinstance(value, str):
            if not value.strip():
                return []
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.environment == "production" and self.jwt_secret_key == "change-this-before-production":
            raise ValueError("JWT_SECRET_KEY must be changed for production deployments.")
        return self

    @property
    def async_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        url = URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )
        return url.render_as_string(hide_password=False)

    @property
    def sync_database_url(self) -> str:
        url = make_url(self.async_database_url)
        drivername = url.drivername.replace("+asyncpg", "+psycopg")
        sync_url = url.set(drivername=drivername)
        return sync_url.render_as_string(hide_password=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
