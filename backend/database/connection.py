import os
from typing import Optional
from contextlib import asynccontextmanager


class Database:
    """Database connection manager."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._connection = None
        self._pool = None

    async def connect(self):
        """Establish database connection."""
        # In production, use asyncpg or motor for async database operations
        print(f"Connecting to database...")
        self._connection = True  # Placeholder

    async def disconnect(self):
        """Close database connection."""
        if self._connection:
            print("Disconnecting from database...")
            self._connection = None

    @property
    def is_connected(self) -> bool:
        return self._connection is not None

    async def execute(self, query: str, *args):
        """Execute a database query."""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        # Placeholder for query execution
        return None

    async def fetch_one(self, query: str, *args):
        """Fetch single row."""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        return None

    async def fetch_all(self, query: str, *args):
        """Fetch all rows."""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        return []


# Global database instance
_database: Optional[Database] = None


def get_database_url() -> str:
    """Get database URL from environment."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://localhost:5432/medical_diagnosis"
    )


async def get_database() -> Database:
    """Get or create database connection."""
    global _database

    if _database is None:
        _database = Database(get_database_url())
        await _database.connect()

    return _database


async def close_database():
    """Close database connection."""
    global _database

    if _database is not None:
        await _database.disconnect()
        _database = None


@asynccontextmanager
async def database_session():
    """Context manager for database sessions."""
    db = await get_database()
    try:
        yield db
    finally:
        pass  # Connection pooling handles cleanup
