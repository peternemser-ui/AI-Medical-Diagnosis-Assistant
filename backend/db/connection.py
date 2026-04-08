"""
PostgreSQL Database Connection Manager

Provides async connection pool for the application.
Falls back to SQLite for development without Docker.
"""

import os
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

# Connection pool (lazy initialized)
_pool = None
_is_postgres = False


def get_database_url():
    """Get database URL from environment."""
    return os.getenv("DATABASE_URL", "")


def is_postgres_available():
    """Check if PostgreSQL is configured and reachable."""
    url = get_database_url()
    if not url or not url.startswith("postgresql"):
        return False
    try:
        import psycopg2
        conn = psycopg2.connect(url, connect_timeout=3)
        conn.close()
        return True
    except Exception as e:
        logger.warning("PostgreSQL not available: %s", e)
        return False


async def init_pool():
    """Initialize the async connection pool."""
    global _pool, _is_postgres
    url = get_database_url()

    if url and url.startswith("postgresql"):
        try:
            import asyncpg
            _pool = await asyncpg.create_pool(
                url,
                min_size=2,
                max_size=10,
                command_timeout=30,
                statement_cache_size=0,  # Disable for pgbouncer compatibility
            )
            _is_postgres = True
            logger.info("PostgreSQL connection pool initialized (min=2, max=10)")
            return True
        except Exception as e:
            logger.error("Failed to initialize PostgreSQL pool: %s", e)
            _is_postgres = False
            return False
    else:
        logger.info("No PostgreSQL URL configured — running without database (in-memory mode)")
        _is_postgres = False
        return False


async def close_pool():
    """Close the connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("PostgreSQL connection pool closed")


@asynccontextmanager
async def get_connection():
    """Get a connection from the pool."""
    if not _pool:
        raise RuntimeError("Database pool not initialized. Call init_pool() first.")
    async with _pool.acquire() as conn:
        yield conn


async def execute(query, *args):
    """Execute a query and return the result."""
    async with get_connection() as conn:
        return await conn.execute(query, *args)


async def fetch(query, *args):
    """Fetch multiple rows."""
    async with get_connection() as conn:
        return await conn.fetch(query, *args)


async def fetchrow(query, *args):
    """Fetch a single row."""
    async with get_connection() as conn:
        return await conn.fetchrow(query, *args)


async def fetchval(query, *args):
    """Fetch a single value."""
    async with get_connection() as conn:
        return await conn.fetchval(query, *args)


def is_connected():
    """Check if the database is connected."""
    return _is_postgres and _pool is not None
