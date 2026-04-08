"""
Alembic environment configuration for AI Medical Diagnosis Assistant.

Reads DATABASE_URL from the environment (or .env file) to connect.
Supports both PostgreSQL (production) and SQLite (development/fallback).

Usage:
    # Apply all pending migrations
    cd backend && python -m alembic upgrade head

    # Generate a new migration (auto-detect schema changes)
    cd backend && python -m alembic revision --autogenerate -m "description"

    # Downgrade one step
    cd backend && python -m alembic downgrade -1
"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Path setup ───────────────────────────────────────────────────────────────
# Add the backend directory to sys.path so SQLAlchemy models can be imported.
_BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND_DIR))

# Load .env so DATABASE_URL is available when running alembic from the CLI.
try:
    from dotenv import load_dotenv
    load_dotenv(_BACKEND_DIR / ".env")
except ImportError:
    pass  # python-dotenv not installed; rely on shell environment

# ── Alembic Config object ─────────────────────────────────────────────────────
config = context.config

# Wire Python logging from alembic.ini [loggers] section.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Target metadata ──────────────────────────────────────────────────────────
# Import SQLAlchemy models here if you want --autogenerate to detect changes.
# Example:
#   from myapp.models import Base
#   target_metadata = Base.metadata
#
# The current project uses raw SQL migrations (init.sql), so autogenerate is
# not wired to models.  Set target_metadata = None to run in manual mode.
target_metadata = None


# ── Database URL resolution ───────────────────────────────────────────────────

def _get_db_url() -> str:
    """
    Return the database URL to use for migrations.

    Priority:
    1. DATABASE_URL environment variable (PostgreSQL for production)
    2. Fallback to local SQLite file (development)
    """
    url = os.getenv("DATABASE_URL", "")
    if url.startswith("postgresql"):
        return url

    # SQLite fallback — same path used by database.py
    sqlite_path = _BACKEND_DIR / "medical_auth.db"
    return f"sqlite:///{sqlite_path}"


# ── Offline migrations ────────────────────────────────────────────────────────

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode (emit SQL to stdout, no live DB connection).

    Useful for generating SQL scripts to review before applying.
    Run with: alembic upgrade head --sql
    """
    url = _get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Render AS for CHECK constraints so they survive round-trips
        render_as_batch=url.startswith("sqlite"),
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online migrations ─────────────────────────────────────────────────────────

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode (connect to the live database).

    This is the default mode used by `alembic upgrade head`.
    """
    url = _get_db_url()

    # Override the sqlalchemy.url from alembic.ini with the resolved URL.
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # NullPool avoids connection leaks in migration scripts
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # batch mode required for SQLite (which doesn't support ALTER TABLE)
            render_as_batch=url.startswith("sqlite"),
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
