from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

BACKEND_DIR = Path(__file__).resolve().parents[1]
ALEMBIC_INI_PATH = BACKEND_DIR / "alembic.ini"
REVISION_ID = "20260622_0001"


def test_alembic_head_revision_matches_initial_migration() -> None:
    config = Config(str(ALEMBIC_INI_PATH))
    script = ScriptDirectory.from_config(config)

    assert script.get_current_head() == REVISION_ID


def test_alembic_upgrade_sql_generation() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", "head", "--sql"],
        cwd=BACKEND_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "CREATE TABLE users" in result.stdout
    assert "CREATE TABLE planets" in result.stdout
    assert "CREATE TABLE nova_messages" in result.stdout
    assert REVISION_ID in result.stdout


def test_alembic_downgrade_sql_generation() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "downgrade", f"{REVISION_ID}:base", "--sql"],
        cwd=BACKEND_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "DROP TABLE nova_messages" in result.stdout
    assert "DROP TABLE users" in result.stdout
    assert "DROP TABLE artifacts" in result.stdout
