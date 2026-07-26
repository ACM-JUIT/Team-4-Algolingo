"""create initial algolingo schema

Revision ID: 20260622_0001
Revises: None
Create Date: 2026-06-22 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260622_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "artifacts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("rarity", sa.String(length=20), nullable=False),
        sa.Column("rarity_color", sa.String(length=20), nullable=True),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("unlock_condition", sa.Text(), nullable=True),
        sa.Column("xp_bonus_percent", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("icon_url", sa.String(length=255), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("display_order >= 0", name=op.f("ck_artifacts_artifacts_display_order_non_negative")),
        sa.CheckConstraint("xp_bonus_percent >= 0", name=op.f("ck_artifacts_artifacts_xp_bonus_non_negative")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_artifacts")),
        sa.UniqueConstraint("name", name=op.f("uq_artifacts_name")),
    )
    op.create_index(op.f("ix_artifacts_category"), "artifacts", ["category"], unique=False)
    op.create_index(op.f("ix_artifacts_name"), "artifacts", ["name"], unique=True)
    op.create_index(op.f("ix_artifacts_rarity"), "artifacts", ["rarity"], unique=False)

    op.create_table(
        "galaxies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("programming_language", sa.String(length=50), nullable=True),
        sa.Column("order_number", sa.Integer(), nullable=False),
        sa.Column("is_locked", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("icon_url", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("order_number >= 1", name=op.f("ck_galaxies_galaxies_order_number_minimum")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_galaxies")),
        sa.UniqueConstraint("name", name=op.f("uq_galaxies_name")),
        sa.UniqueConstraint("order_number", name=op.f("uq_galaxies_order_number")),
    )
    op.create_index(op.f("ix_galaxies_name"), "galaxies", ["name"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("avatar_url", sa.String(length=255), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("xp", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("level", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("rank_title", sa.String(length=50), server_default=sa.text("'Cadet'"), nullable=False),
        sa.Column("streak_days", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("last_login_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), server_default=sa.text("'ACTIVE'"), nullable=False),
        sa.Column("role", sa.String(length=20), server_default=sa.text("'USER'"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("level >= 1", name=op.f("ck_users_users_level_minimum")),
        sa.CheckConstraint("xp >= 0", name=op.f("ck_users_users_xp_non_negative")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)
    op.create_index(op.f("ix_users_status"), "users", ["status"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_index("ix_users_xp_desc", "users", [sa.text("xp DESC")], unique=False)

    op.create_table(
        "planets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("galaxy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("artifact_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("tagline", sa.String(length=200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("difficulty", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("order_number", sa.Integer(), nullable=False),
        sa.Column("xp_total", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("estimated_time_minutes", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("unlock_condition", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "difficulty >= 1 AND difficulty <= 5",
            name=op.f("ck_planets_planets_difficulty_range"),
        ),
        sa.CheckConstraint(
            "estimated_time_minutes IS NULL OR estimated_time_minutes >= 0",
            name=op.f("ck_planets_planets_estimated_time_non_negative"),
        ),
        sa.CheckConstraint("xp_total >= 0", name=op.f("ck_planets_planets_xp_total_non_negative")),
        sa.ForeignKeyConstraint(["artifact_id"], ["artifacts.id"], name=op.f("fk_planets_artifact_id_artifacts"), ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["galaxy_id"], ["galaxies.id"], name=op.f("fk_planets_galaxy_id_galaxies"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_planets")),
        sa.UniqueConstraint("galaxy_id", "order_number", name="uq_planets_galaxy_order_number"),
    )
    op.create_index(op.f("ix_planets_galaxy_id"), "planets", ["galaxy_id"], unique=False)
    op.create_index(op.f("ix_planets_status"), "planets", ["status"], unique=False)

    op.create_table(
        "daily_logins",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("login_date", sa.Date(), nullable=False),
        sa.Column("xp_earned", sa.Integer(), server_default=sa.text("25"), nullable=False),
        sa.Column("streak_day", sa.Integer(), nullable=False),
        sa.CheckConstraint("streak_day >= 1", name=op.f("ck_daily_logins_daily_logins_streak_day_minimum")),
        sa.CheckConstraint("xp_earned >= 0", name=op.f("ck_daily_logins_daily_logins_xp_earned_non_negative")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_daily_logins_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_daily_logins")),
        sa.UniqueConstraint("user_id", "login_date", name="uq_daily_logins_user_date"),
    )
    op.create_index(op.f("ix_daily_logins_user_id"), "daily_logins", ["user_id"], unique=False)

    op.create_table(
        "discoveries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("planet_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("content_md", sa.Text(), nullable=True),
        sa.Column("learning_objective", sa.Text(), nullable=True),
        sa.Column("read_time_minutes", sa.Integer(), nullable=True),
        sa.Column("difficulty", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("xp_reward", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("order_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("prerequisites", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "difficulty >= 1 AND difficulty <= 5",
            name=op.f("ck_discoveries_discoveries_difficulty_range"),
        ),
        sa.CheckConstraint(
            "read_time_minutes IS NULL OR read_time_minutes >= 0",
            name=op.f("ck_discoveries_discoveries_read_time_non_negative"),
        ),
        sa.CheckConstraint("xp_reward >= 0", name=op.f("ck_discoveries_discoveries_xp_reward_non_negative")),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], name=op.f("fk_discoveries_planet_id_planets"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_discoveries")),
        sa.UniqueConstraint("planet_id", "order_number", name="uq_discoveries_planet_order_number"),
    )
    op.create_index(op.f("ix_discoveries_planet_id"), "discoveries", ["planet_id"], unique=False)
    op.create_index(op.f("ix_discoveries_status"), "discoveries", ["status"], unique=False)

    op.create_table(
        "leaderboard_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("leaderboard_type", sa.String(length=20), nullable=False),
        sa.Column("rank_position", sa.Integer(), nullable=False),
        sa.Column("xp", sa.Integer(), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "rank_position >= 1",
            name=op.f("ck_leaderboard_snapshots_leaderboard_snapshots_rank_position_minimum"),
        ),
        sa.CheckConstraint("xp >= 0", name=op.f("ck_leaderboard_snapshots_leaderboard_snapshots_xp_non_negative")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_leaderboard_snapshots_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leaderboard_snapshots")),
    )
    op.create_index(op.f("ix_leaderboard_snapshots_leaderboard_type"), "leaderboard_snapshots", ["leaderboard_type"], unique=False)
    op.create_index(
        "ix_leaderboard_snapshots_type_date_rank",
        "leaderboard_snapshots",
        ["leaderboard_type", "snapshot_date", "rank_position"],
        unique=False,
    )
    op.create_index(op.f("ix_leaderboard_snapshots_snapshot_date"), "leaderboard_snapshots", ["snapshot_date"], unique=False)
    op.create_index(op.f("ix_leaderboard_snapshots_user_id"), "leaderboard_snapshots", ["user_id"], unique=False)

    op.create_table(
        "nova_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_nova_sessions_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_nova_sessions")),
    )
    op.create_index(op.f("ix_nova_sessions_user_id"), "nova_sessions", ["user_id"], unique=False)

    op.create_table(
        "practice_challenges",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("planet_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("challenge_type", sa.String(length=50), nullable=False),
        sa.Column("difficulty", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("learning_outcome", sa.Text(), nullable=True),
        sa.Column("xp_reward", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("solution_code", sa.Text(), nullable=True),
        sa.Column("hints", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("test_cases", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("order_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "difficulty >= 1 AND difficulty <= 5",
            name=op.f("ck_practice_challenges_practice_challenges_difficulty_range"),
        ),
        sa.CheckConstraint(
            "xp_reward >= 0",
            name=op.f("ck_practice_challenges_practice_challenges_xp_reward_non_negative"),
        ),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], name=op.f("fk_practice_challenges_planet_id_planets"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_practice_challenges")),
        sa.UniqueConstraint("planet_id", "order_number", name="uq_practice_challenges_planet_order_number"),
    )
    op.create_index(op.f("ix_practice_challenges_challenge_type"), "practice_challenges", ["challenge_type"], unique=False)
    op.create_index(op.f("ix_practice_challenges_planet_id"), "practice_challenges", ["planet_id"], unique=False)
    op.create_index(op.f("ix_practice_challenges_status"), "practice_challenges", ["status"], unique=False)

    op.create_table(
        "quiz_questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("planet_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(length=50), nullable=False),
        sa.Column("options", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("correct_answer", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("difficulty", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("xp_reward", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("order_number", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "difficulty >= 1 AND difficulty <= 5",
            name=op.f("ck_quiz_questions_quiz_questions_difficulty_range"),
        ),
        sa.CheckConstraint("xp_reward >= 0", name=op.f("ck_quiz_questions_quiz_questions_xp_reward_non_negative")),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], name=op.f("fk_quiz_questions_planet_id_planets"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_quiz_questions")),
        sa.UniqueConstraint("planet_id", "order_number", name="uq_quiz_questions_planet_order_number"),
    )
    op.create_index(op.f("ix_quiz_questions_planet_id"), "quiz_questions", ["planet_id"], unique=False)
    op.create_index(op.f("ix_quiz_questions_question_type"), "quiz_questions", ["question_type"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("revoked", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_refresh_tokens_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_tokens")),
        sa.UniqueConstraint("token_hash", name=op.f("uq_refresh_tokens_token_hash")),
    )
    op.create_index(op.f("ix_refresh_tokens_token_hash"), "refresh_tokens", ["token_hash"], unique=True)
    op.create_index(op.f("ix_refresh_tokens_user_id"), "refresh_tokens", ["user_id"], unique=False)
    op.create_index("ix_refresh_tokens_user_revoked", "refresh_tokens", ["user_id", "revoked"], unique=False)

    op.create_table(
        "user_artifacts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("artifact_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("showcased", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["artifact_id"], ["artifacts.id"], name=op.f("fk_user_artifacts_artifact_id_artifacts"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_user_artifacts_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_artifacts")),
        sa.UniqueConstraint("user_id", "artifact_id", name="uq_user_artifacts_user_artifact"),
    )
    op.create_index(op.f("ix_user_artifacts_artifact_id"), "user_artifacts", ["artifact_id"], unique=False)
    op.create_index(op.f("ix_user_artifacts_user_id"), "user_artifacts", ["user_id"], unique=False)

    op.create_table(
        "user_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("event_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_user_events_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_events")),
    )
    op.create_index(op.f("ix_user_events_event_type"), "user_events", ["event_type"], unique=False)
    op.create_index("ix_user_events_user_type_created", "user_events", ["user_id", "event_type", "created_at"], unique=False)
    op.create_index(op.f("ix_user_events_user_id"), "user_events", ["user_id"], unique=False)

    op.create_table(
        "user_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("planet_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("completed_discoveries", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("completed_practices", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("quiz_passed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("quiz_best_score", sa.Integer(), nullable=True),
        sa.Column("completed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("xp_earned", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "quiz_best_score IS NULL OR quiz_best_score >= 0",
            name=op.f("ck_user_progress_user_progress_quiz_best_score_non_negative"),
        ),
        sa.CheckConstraint("xp_earned >= 0", name=op.f("ck_user_progress_user_progress_xp_earned_non_negative")),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], name=op.f("fk_user_progress_planet_id_planets"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_user_progress_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_progress")),
        sa.UniqueConstraint("user_id", "planet_id", name="uq_user_progress_user_planet"),
    )
    op.create_index(op.f("ix_user_progress_planet_id"), "user_progress", ["planet_id"], unique=False)
    op.create_index(op.f("ix_user_progress_status"), "user_progress", ["status"], unique=False)
    op.create_index(op.f("ix_user_progress_user_id"), "user_progress", ["user_id"], unique=False)

    op.create_table(
        "quiz_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("planet_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column("answers", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("passed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("xp_earned", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("attempted_at", sa.DateTime(timezone=False), nullable=False),
        sa.CheckConstraint("score >= 0", name=op.f("ck_quiz_attempts_quiz_attempts_score_non_negative")),
        sa.CheckConstraint(
            "total_questions >= 0",
            name=op.f("ck_quiz_attempts_quiz_attempts_total_questions_non_negative"),
        ),
        sa.CheckConstraint("xp_earned >= 0", name=op.f("ck_quiz_attempts_quiz_attempts_xp_earned_non_negative")),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], name=op.f("fk_quiz_attempts_planet_id_planets"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_quiz_attempts_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_quiz_attempts")),
    )
    op.create_index(op.f("ix_quiz_attempts_planet_id"), "quiz_attempts", ["planet_id"], unique=False)
    op.create_index(op.f("ix_quiz_attempts_user_id"), "quiz_attempts", ["user_id"], unique=False)

    op.create_table(
        "nova_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sender", sa.String(length=20), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("context_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["nova_sessions.id"], name=op.f("fk_nova_messages_session_id_nova_sessions"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_nova_messages")),
    )
    op.create_index(op.f("ix_nova_messages_sender"), "nova_messages", ["sender"], unique=False)
    op.create_index(op.f("ix_nova_messages_session_id"), "nova_messages", ["session_id"], unique=False)


def downgrade() -> None:
    op.drop_table("nova_messages")
    op.drop_table("quiz_attempts")
    op.drop_table("user_progress")
    op.drop_table("user_events")
    op.drop_table("user_artifacts")
    op.drop_table("refresh_tokens")
    op.drop_table("quiz_questions")
    op.drop_table("practice_challenges")
    op.drop_table("nova_sessions")
    op.drop_table("leaderboard_snapshots")
    op.drop_table("discoveries")
    op.drop_table("daily_logins")
    op.drop_table("planets")
    op.drop_table("users")
    op.drop_table("galaxies")
    op.drop_table("artifacts")
