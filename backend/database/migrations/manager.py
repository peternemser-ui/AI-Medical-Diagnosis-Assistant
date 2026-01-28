from datetime import datetime
from typing import List, Optional
import os


class Migration:
    """Represents a database migration."""

    def __init__(self, version: str, name: str, up_sql: str, down_sql: str):
        self.version = version
        self.name = name
        self.up_sql = up_sql
        self.down_sql = down_sql
        self.applied_at: Optional[datetime] = None


class MigrationManager:
    """Manages database migrations."""

    def __init__(self, database):
        self.database = database
        self._migrations: List[Migration] = []
        self._applied: List[str] = []

    async def initialize(self):
        """Initialize migration tracking table."""
        await self.database.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                version VARCHAR(50) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Load applied migrations
        rows = await self.database.fetch_all(
            "SELECT version FROM _migrations ORDER BY version"
        )
        self._applied = [row['version'] for row in rows]

    def register(self, migration: Migration):
        """Register a migration."""
        self._migrations.append(migration)
        self._migrations.sort(key=lambda m: m.version)

    async def migrate(self, target_version: Optional[str] = None):
        """Run pending migrations up to target version."""
        pending = [
            m for m in self._migrations
            if m.version not in self._applied
        ]

        if target_version:
            pending = [m for m in pending if m.version <= target_version]

        for migration in pending:
            print(f"Applying migration {migration.version}: {migration.name}")

            await self.database.execute(migration.up_sql)

            await self.database.execute(
                "INSERT INTO _migrations (version, name) VALUES ($1, $2)",
                migration.version,
                migration.name
            )

            self._applied.append(migration.version)
            migration.applied_at = datetime.utcnow()

        return len(pending)

    async def rollback(self, steps: int = 1):
        """Rollback migrations."""
        applied = [
            m for m in self._migrations
            if m.version in self._applied
        ]
        applied.reverse()

        rolled_back = 0
        for migration in applied[:steps]:
            print(f"Rolling back migration {migration.version}: {migration.name}")

            await self.database.execute(migration.down_sql)

            await self.database.execute(
                "DELETE FROM _migrations WHERE version = $1",
                migration.version
            )

            self._applied.remove(migration.version)
            rolled_back += 1

        return rolled_back

    async def status(self) -> List[dict]:
        """Get migration status."""
        status = []
        for migration in self._migrations:
            status.append({
                'version': migration.version,
                'name': migration.name,
                'applied': migration.version in self._applied,
                'applied_at': migration.applied_at
            })
        return status

    def get_pending(self) -> List[Migration]:
        """Get pending migrations."""
        return [m for m in self._migrations if m.version not in self._applied]


# Pre-defined migrations
MIGRATIONS = [
    Migration(
        version="001",
        name="create_users_table",
        up_sql="""
            CREATE TABLE users (
                id UUID PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'patient',
                email_verified BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                date_of_birth DATE,
                gender VARCHAR(20),
                phone VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_users_email ON users(email);
        """,
        down_sql="DROP TABLE IF EXISTS users;"
    ),
    Migration(
        version="002",
        name="create_sessions_table",
        up_sql="""
            CREATE TABLE sessions (
                id UUID PRIMARY KEY,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                token VARCHAR(500) NOT NULL,
                device_info TEXT,
                ip_address VARCHAR(45),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_sessions_user ON sessions(user_id);
            CREATE INDEX idx_sessions_token ON sessions(token);
        """,
        down_sql="DROP TABLE IF EXISTS sessions;"
    ),
    Migration(
        version="003",
        name="create_diagnoses_table",
        up_sql="""
            CREATE TABLE diagnoses (
                id UUID PRIMARY KEY,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                symptoms JSONB NOT NULL,
                symptom_description TEXT,
                conditions JSONB,
                recommendations JSONB,
                urgency VARCHAR(20),
                red_flags JSONB,
                status VARCHAR(20) DEFAULT 'pending',
                ai_model VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_by UUID REFERENCES users(id),
                reviewed_at TIMESTAMP,
                review_notes TEXT
            );
            CREATE INDEX idx_diagnoses_user ON diagnoses(user_id);
            CREATE INDEX idx_diagnoses_status ON diagnoses(status);
            CREATE INDEX idx_diagnoses_urgency ON diagnoses(urgency);
        """,
        down_sql="DROP TABLE IF EXISTS diagnoses;"
    ),
    Migration(
        version="004",
        name="create_medical_history_table",
        up_sql="""
            CREATE TABLE medical_history (
                id UUID PRIMARY KEY,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                diagnosis_id UUID REFERENCES diagnoses(id),
                entry_type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                date TIMESTAMP NOT NULL,
                provider VARCHAR(255),
                notes TEXT,
                attachments JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_history_user ON medical_history(user_id);
            CREATE INDEX idx_history_type ON medical_history(entry_type);
            CREATE INDEX idx_history_date ON medical_history(date);
        """,
        down_sql="DROP TABLE IF EXISTS medical_history;"
    ),
    Migration(
        version="005",
        name="create_conversations_table",
        up_sql="""
            CREATE TABLE conversations (
                id UUID PRIMARY KEY,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                diagnosis_id UUID REFERENCES diagnoses(id),
                messages JSONB NOT NULL DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_conversations_user ON conversations(user_id);
        """,
        down_sql="DROP TABLE IF EXISTS conversations;"
    )
]
