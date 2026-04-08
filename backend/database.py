"""
Database layer with PostgreSQL (primary) and SQLite (fallback) support.

PostgreSQL mode: Uses psycopg2 with ThreadedConnectionPool and the schema
from db/init.sql (email_hash, email_encrypted, etc.).

SQLite mode: Activated when DATABASE_URL is not set or PostgreSQL is
unreachable.  Uses threading.Lock and a simpler schema matching the old
column layout.

All PII (email, name, symptoms, diagnosis results, profile data) is encrypted
at rest using Fernet symmetric encryption.  Passwords are hashed with bcrypt.
Audit logging tracks every sensitive action for HIPAA compliance.
"""

import os
import json
import sqlite3
import uuid
import logging
import threading
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Encryption — delegate to db/encryption.py
# ---------------------------------------------------------------------------

try:
    from db.encryption import (
        encrypt,
        decrypt,
        hash_for_lookup,
        encrypt_json,
        decrypt_json,
    )
except ImportError:
    # Fallback: if db.encryption is not available, define locally
    from cryptography.fernet import Fernet as _Fernet

    def _load_or_create_key(env_var: str = "ENCRYPTION_KEY") -> bytes:
        key = os.getenv(env_var)
        if key:
            return key.encode()
        new_key = _Fernet.generate_key()
        _append_env(env_var, new_key.decode())
        os.environ[env_var] = new_key.decode()
        return new_key

    _fernet = _Fernet(_load_or_create_key())

    def encrypt(value):
        if value is None:
            return None
        return _fernet.encrypt(str(value).encode()).decode()

    def decrypt(value):
        if value is None:
            return None
        try:
            return _fernet.decrypt(value.encode()).decode()
        except Exception:
            return value

    def hash_for_lookup(value):
        import hashlib
        if value is None:
            return None
        return hashlib.sha256(value.strip().lower().encode()).hexdigest()

    def encrypt_json(data):
        if data is None:
            return None
        return encrypt(json.dumps(data))

    def decrypt_json(ciphertext):
        if ciphertext is None:
            return None
        try:
            pt = decrypt(ciphertext)
            return json.loads(pt)
        except Exception:
            return None


# ---------------------------------------------------------------------------
# .env helper (still needed by auth.py which imports _append_env)
# ---------------------------------------------------------------------------

_ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")


def _append_env(name: str, value: str) -> None:
    """Append a key=value line to the backend/.env file (create if missing)."""
    line = f"{name}={value}\n"
    existing = ""
    if os.path.exists(_ENV_FILE):
        with open(_ENV_FILE, "r") as f:
            existing = f.read()
    if f"{name}=" not in existing:
        with open(_ENV_FILE, "a") as f:
            f.write(line)


# ---------------------------------------------------------------------------
# Detect database mode
# ---------------------------------------------------------------------------

def _is_pg_configured() -> bool:
    url = os.getenv("DATABASE_URL", "")
    return url.startswith("postgresql")


# ---------------------------------------------------------------------------
# Database class
# ---------------------------------------------------------------------------

_DB_PATH = os.path.join(os.path.dirname(__file__), "medical_auth.db")


class Database:
    """Unified database layer — PostgreSQL (production) or SQLite (dev)."""

    _instance: Optional["Database"] = None
    _lock = threading.Lock()

    def __init__(self, db_path: str = _DB_PATH):
        self.db_path = db_path
        self._use_pg = False
        self._pg_pool = None
        self._sqlite_lock = threading.Lock()
        self._local = threading.local()

        if _is_pg_configured():
            try:
                import psycopg2
                import psycopg2.pool
                url = os.getenv("DATABASE_URL")
                self._pg_pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=10,
                    dsn=url,
                )
                self._use_pg = True
                logger.info("Database: PostgreSQL mode (pool 1–10)")
                self._init_pg_tables()
            except Exception as exc:
                logger.warning("PostgreSQL unavailable (%s) — falling back to SQLite", exc)
                self._use_pg = False
                self._init_sqlite_tables()
        else:
            logger.info("Database: SQLite mode (%s)", db_path)
            self._init_sqlite_tables()

    # -- singleton ----------------------------------------------------------

    @classmethod
    def get(cls) -> "Database":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # -- connection helpers -------------------------------------------------

    def _pg_conn(self):
        """Get a psycopg2 connection from the pool."""
        return self._pg_pool.getconn()

    def _pg_put(self, conn):
        """Return a psycopg2 connection to the pool."""
        self._pg_pool.putconn(conn)

    def _conn(self) -> sqlite3.Connection:
        """Return a thread-local SQLite connection (for SQLite mode).

        Also used directly by auth_routes.py change_password endpoint, so
        this must remain accessible even in PG mode — in PG mode it returns
        a thin wrapper that lets callers do conn.execute(...) / conn.commit().
        """
        if self._use_pg:
            # Return a lightweight proxy so that external code calling
            # db._conn().execute(sql, params) still works against PG.
            return _PgConnProxy(self)

        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA foreign_keys=ON")
        return self._local.conn

    # -- schema initialisation ---------------------------------------------

    def _init_pg_tables(self) -> None:
        """Create tables in PostgreSQL if they don't exist."""
        conn = self._pg_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.users')")
                if cur.fetchone()[0] is not None:
                    conn.commit()
                    return  # Tables already exist

                # Try loading from init.sql
                init_sql = os.path.join(os.path.dirname(__file__), "db", "init.sql")
                if os.path.exists(init_sql):
                    with open(init_sql, "r") as f:
                        sql = f.read()
                    cur.execute(sql)
                else:
                    # Inline minimal schema matching init.sql column names
                    cur.execute(self._pg_schema_sql())
                conn.commit()
                logger.info("PostgreSQL tables initialised")
        except Exception as exc:
            conn.rollback()
            logger.error("Failed to init PG tables: %s", exc)
            raise
        finally:
            self._pg_put(conn)

    @staticmethod
    def _pg_schema_sql() -> str:
        return """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email_hash TEXT UNIQUE NOT NULL,
            email_encrypted TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'patient',
            name_encrypted TEXT,
            phone_encrypted TEXT,
            date_of_birth_encrypted TEXT,
            profile_data_encrypted TEXT,
            preferred_language TEXT DEFAULT 'en',
            timezone TEXT DEFAULT 'UTC',
            subscription_tier TEXT DEFAULT 'free',
            stripe_customer_id TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            last_login_at TIMESTAMPTZ,
            email_verified_at TIMESTAMPTZ,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
            failed_login_attempts INTEGER NOT NULL DEFAULT 0,
            locked_until TIMESTAMPTZ,
            hipaa_consent_at TIMESTAMPTZ,
            terms_accepted_at TIMESTAMPTZ
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token_hash TEXT NOT NULL,
            device_fingerprint TEXT,
            ip_address INET,
            user_agent TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            expires_at TIMESTAMPTZ NOT NULL,
            last_used_at TIMESTAMPTZ,
            is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
            revoked_at TIMESTAMPTZ,
            revoke_reason TEXT
        );

        CREATE TABLE IF NOT EXISTS diagnoses (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            symptoms_encrypted TEXT NOT NULL,
            chief_complaint_encrypted TEXT,
            age INTEGER,
            gender TEXT,
            severity INTEGER,
            duration TEXT,
            result_encrypted TEXT,
            specialist_routing JSONB,
            model_used TEXT,
            agents_used TEXT[],
            agent_timings JSONB,
            estimated_cost DECIMAL(10,4),
            total_time DECIMAL(10,2),
            status TEXT NOT NULL DEFAULT 'completed',
            urgency TEXT DEFAULT 'routine',
            confidence_score INTEGER,
            reviewed_by UUID REFERENCES users(id),
            reviewed_at TIMESTAMPTZ,
            review_notes_encrypted TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            completed_at TIMESTAMPTZ,
            has_image BOOLEAN DEFAULT FALSE,
            image_analysis_status TEXT
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id BIGSERIAL PRIMARY KEY,
            user_id UUID,
            session_id UUID,
            action TEXT NOT NULL,
            resource_type TEXT,
            resource_id TEXT,
            ip_address INET,
            user_agent TEXT,
            old_value_encrypted TEXT,
            new_value_encrypted TEXT,
            details JSONB,
            severity TEXT DEFAULT 'info',
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """

    def _init_sqlite_tables(self) -> None:
        conn = self._conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'patient',
                name TEXT,
                created_at TEXT NOT NULL,
                last_login TEXT,
                is_active BOOLEAN DEFAULT 1,
                profile_data TEXT,
                email_verified BOOLEAN DEFAULT 0,
                verification_token TEXT
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                token_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                is_revoked BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS diagnoses (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                symptoms TEXT,
                age INTEGER,
                gender TEXT,
                result_data TEXT,
                specialist_routing TEXT,
                model_used TEXT,
                estimated_cost REAL,
                total_time REAL,
                status TEXT DEFAULT 'completed',
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT NOT NULL,
                resource TEXT,
                ip_address TEXT,
                timestamp TEXT NOT NULL,
                details TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_diagnoses_user ON diagnoses(user_id);
            CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
            CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_log(timestamp);
        """)
        conn.commit()
        # Migrate older schemas: add email verification columns if missing
        self._migrate_sqlite_email_verification(conn)

    def _migrate_sqlite_email_verification(self, conn) -> None:
        """Add email_verified and verification_token columns to existing databases."""
        existing = {row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
        if "email_verified" not in existing:
            conn.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT 0")
            logger.info("SQLite migration: added email_verified column")
        if "verification_token" not in existing:
            conn.execute("ALTER TABLE users ADD COLUMN verification_token TEXT")
            logger.info("SQLite migration: added verification_token column")
        conn.commit()

    # ======================================================================
    # USER CRUD
    # ======================================================================

    def create_user(self, email: str, password: str, name: str = "",
                    role: str = "patient",
                    verification_token: str = None) -> dict:
        """Create a new user with encrypted PII and bcrypt-hashed password.

        If verification_token is provided it is stored so the user can
        verify their email address via GET /api/auth/verify-email?token=xxx.
        """
        import bcrypt

        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        if self._use_pg:
            email_hashed = hash_for_lookup(email)
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO users
                           (id, email_hash, email_encrypted, password_hash,
                            role, name_encrypted, created_at,
                            is_email_verified)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (user_id, email_hashed, encrypt(email), pw_hash,
                         role, encrypt(name), now, False),
                    )
                conn.commit()
                # Store verification token in a separate update so PG schema
                # differences don't break the INSERT on older migrations.
                if verification_token:
                    self._pg_set_verification_token(user_id, verification_token, conn_override=None)
            except Exception as exc:
                conn.rollback()
                if "duplicate key" in str(exc).lower() or "unique" in str(exc).lower():
                    raise ValueError("An account with this email already exists")
                raise
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            try:
                with self._sqlite_lock:
                    conn.execute(
                        """INSERT INTO users
                           (id, email, password_hash, role, name, created_at,
                            email_verified, verification_token)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (user_id, encrypt(email), pw_hash, role,
                         encrypt(name), now, 0, verification_token),
                    )
                    conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError("An account with this email already exists")

        return {
            "id": user_id,
            "email": email,
            "name": name,
            "role": role,
            "created_at": now,
            "is_active": True,
            "email_verified": False,
            "profile_data": None,
        }

    def authenticate(self, email: str, password: str) -> Optional[dict]:
        """Verify email + password. Returns user dict or None."""
        import bcrypt

        if self._use_pg:
            email_hashed = hash_for_lookup(email)
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM users WHERE email_hash = %s AND is_active = TRUE",
                        (email_hashed,),
                    )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    row = cur.fetchone()
                if row is None:
                    return None
                row_dict = dict(zip(cols, row))
                if bcrypt.checkpw(password.encode(), row_dict["password_hash"].encode()):
                    now = datetime.now(timezone.utc).isoformat()
                    with conn.cursor() as cur:
                        cur.execute(
                            "UPDATE users SET last_login_at = %s WHERE id = %s",
                            (now, str(row_dict["id"])),
                        )
                    conn.commit()
                    return self._pg_row_to_user(row_dict)
                return None
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            rows = conn.execute("SELECT * FROM users WHERE is_active = 1").fetchall()
            for row in rows:
                decrypted_email = decrypt(row["email"])
                if decrypted_email and decrypted_email.lower() == email.lower():
                    if bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
                        now = datetime.now(timezone.utc).isoformat()
                        conn.execute(
                            "UPDATE users SET last_login = ? WHERE id = ?",
                            (now, row["id"]),
                        )
                        conn.commit()
                        return self._sqlite_row_to_user(row)
                    return None
            return None

    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user by ID with decrypted fields."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                    cols = [d[0] for d in cur.description] if cur.description else []
                    row = cur.fetchone()
                if row is None:
                    return None
                return self._pg_row_to_user(dict(zip(cols, row)))
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row is None:
                return None
            return self._sqlite_row_to_user(row)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Look up a user by email address."""
        if self._use_pg:
            email_hashed = hash_for_lookup(email)
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM users WHERE email_hash = %s",
                        (email_hashed,),
                    )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    row = cur.fetchone()
                if row is None:
                    return None
                return self._pg_row_to_user(dict(zip(cols, row)))
            finally:
                self._pg_put(conn)
        else:
            # SQLite: scan and decrypt (no hash column)
            conn = self._conn()
            rows = conn.execute("SELECT * FROM users").fetchall()
            for row in rows:
                decrypted = decrypt(row["email"])
                if decrypted and decrypted.lower() == email.lower():
                    return self._sqlite_row_to_user(row)
            return None

    def update_user(self, user_id: str, data: dict) -> Optional[dict]:
        """Update user profile. Encrypts PII fields."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                sets = []
                params = []
                if "name" in data:
                    sets.append("name_encrypted = %s")
                    params.append(encrypt(data["name"]))
                if "email" in data:
                    sets.append("email_encrypted = %s")
                    params.append(encrypt(data["email"]))
                    sets.append("email_hash = %s")
                    params.append(hash_for_lookup(data["email"]))
                if "role" in data:
                    sets.append("role = %s")
                    params.append(data["role"])
                if "profile_data" in data:
                    sets.append("profile_data_encrypted = %s")
                    pd = data["profile_data"]
                    params.append(encrypt_json(pd) if isinstance(pd, dict) else encrypt(pd))
                if "is_active" in data:
                    sets.append("is_active = %s")
                    params.append(bool(data["is_active"]))
                if "password_hash" in data:
                    sets.append("password_hash = %s")
                    params.append(data["password_hash"])

                if not sets:
                    return self.get_user(user_id)

                params.append(user_id)
                sql = f"UPDATE users SET {', '.join(sets)} WHERE id = %s"
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._pg_put(conn)

            return self.get_user(user_id)
        else:
            conn = self._conn()
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row is None:
                return None

            sets = []
            params = []
            if "name" in data:
                sets.append("name = ?")
                params.append(encrypt(data["name"]))
            if "email" in data:
                sets.append("email = ?")
                params.append(encrypt(data["email"]))
            if "role" in data:
                sets.append("role = ?")
                params.append(data["role"])
            if "profile_data" in data:
                sets.append("profile_data = ?")
                pd = data["profile_data"]
                params.append(encrypt_json(pd) if isinstance(pd, dict) else encrypt(pd))
            if "is_active" in data:
                sets.append("is_active = ?")
                params.append(1 if data["is_active"] else 0)
            if "password_hash" in data:
                sets.append("password_hash = ?")
                params.append(data["password_hash"])

            if not sets:
                return self._sqlite_row_to_user(row)

            params.append(user_id)
            conn.execute(f"UPDATE users SET {', '.join(sets)} WHERE id = ?", params)
            conn.commit()
            return self.get_user(user_id)

    # ======================================================================
    # EMAIL VERIFICATION
    # ======================================================================

    def get_user_by_verification_token(self, token: str) -> Optional[dict]:
        """Look up a user by their email verification token."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    # verification_token stored in profile_data or a dedicated column
                    # We store it in a JSON side-channel via profile_data_encrypted for PG
                    # to avoid a schema migration on existing PG deployments.
                    cur.execute(
                        "SELECT * FROM users WHERE is_active = TRUE",
                        (),
                    )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    rows = cur.fetchall()
                for row in rows:
                    row_dict = dict(zip(cols, row))
                    profile = None
                    if row_dict.get("profile_data_encrypted"):
                        profile = decrypt_json(row_dict["profile_data_encrypted"])
                    if isinstance(profile, dict) and profile.get("_verification_token") == token:
                        return self._pg_row_to_user(row_dict)
                return None
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            row = conn.execute(
                "SELECT * FROM users WHERE verification_token = ? AND is_active = 1",
                (token,),
            ).fetchone()
            if row is None:
                return None
            return self._sqlite_row_to_user(row)

    def set_email_verified(self, user_id: str) -> None:
        """Mark a user's email as verified and clear the verification token."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                now = datetime.now(timezone.utc).isoformat()
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE users SET is_email_verified = TRUE, email_verified_at = %s WHERE id = %s",
                        (now, user_id),
                    )
                    # Also clear the token stored in profile_data
                    cur.execute(
                        "SELECT profile_data_encrypted FROM users WHERE id = %s",
                        (user_id,),
                    )
                    row = cur.fetchone()
                    if row and row[0]:
                        profile = decrypt_json(row[0])
                        if isinstance(profile, dict):
                            profile.pop("_verification_token", None)
                            cur.execute(
                                "UPDATE users SET profile_data_encrypted = %s WHERE id = %s",
                                (encrypt_json(profile), user_id),
                            )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            with self._sqlite_lock:
                conn.execute(
                    "UPDATE users SET email_verified = 1, verification_token = NULL WHERE id = ?",
                    (user_id,),
                )
                conn.commit()

    def set_verification_token(self, user_id: str, token: str) -> None:
        """Store (or replace) an email verification token for a user."""
        if self._use_pg:
            self._pg_set_verification_token(user_id, token)
        else:
            conn = self._conn()
            with self._sqlite_lock:
                conn.execute(
                    "UPDATE users SET verification_token = ?, email_verified = 0 WHERE id = ?",
                    (token, user_id),
                )
                conn.commit()

    def _pg_set_verification_token(self, user_id: str, token: str,
                                    conn_override=None) -> None:
        """Store a verification token inside profile_data_encrypted for PostgreSQL."""
        conn = conn_override or self._pg_conn()
        own_conn = conn_override is None
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT profile_data_encrypted FROM users WHERE id = %s",
                    (user_id,),
                )
                row = cur.fetchone()
                profile = {}
                if row and row[0]:
                    profile = decrypt_json(row[0]) or {}
                profile["_verification_token"] = token
                cur.execute(
                    "UPDATE users SET profile_data_encrypted = %s WHERE id = %s",
                    (encrypt_json(profile), user_id),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if own_conn:
                self._pg_put(conn)

    # -- row converters ----------------------------------------------------

    def _pg_row_to_user(self, row: dict) -> dict:
        profile = None
        if row.get("profile_data_encrypted"):
            profile = decrypt_json(row["profile_data_encrypted"])

        return {
            "id": str(row["id"]),
            "email": decrypt(row["email_encrypted"]),
            "name": decrypt(row["name_encrypted"]) if row.get("name_encrypted") else "",
            "role": row["role"],
            "created_at": row["created_at"].isoformat() if hasattr(row["created_at"], "isoformat") else str(row["created_at"]),
            "last_login": row.get("last_login_at").isoformat() if row.get("last_login_at") and hasattr(row["last_login_at"], "isoformat") else (str(row["last_login_at"]) if row.get("last_login_at") else None),
            "is_active": bool(row["is_active"]),
            "email_verified": bool(row.get("is_email_verified", False)),
            "profile_data": profile,
        }

    def _sqlite_row_to_user(self, row: sqlite3.Row) -> dict:
        profile = None
        if row["profile_data"]:
            profile = decrypt_json(row["profile_data"])

        # email_verified column may not exist on very old DBs — handle gracefully
        try:
            ev = bool(row["email_verified"])
        except (IndexError, KeyError):
            ev = False

        return {
            "id": row["id"],
            "email": decrypt(row["email"]),
            "name": decrypt(row["name"]) if row["name"] else "",
            "role": row["role"],
            "created_at": row["created_at"],
            "last_login": row["last_login"],
            "is_active": bool(row["is_active"]),
            "email_verified": ev,
            "profile_data": profile,
        }

    # ======================================================================
    # DIAGNOSIS STORAGE
    # ======================================================================

    def save_diagnosis(self, user_id: str, diagnosis_data: dict) -> dict:
        """Save an encrypted diagnosis result."""
        diag_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO diagnoses
                           (id, user_id, symptoms_encrypted, age, gender,
                            result_encrypted, specialist_routing, model_used,
                            estimated_cost, total_time, status, created_at)
                           VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s, %s)""",
                        (
                            diag_id,
                            user_id,
                            encrypt(diagnosis_data.get("symptoms", "")),
                            diagnosis_data.get("age"),
                            diagnosis_data.get("gender"),
                            encrypt_json(diagnosis_data.get("result", {})),
                            json.dumps(diagnosis_data.get("specialist_routing", [])),
                            diagnosis_data.get("model_used", ""),
                            diagnosis_data.get("estimated_cost", 0.0),
                            diagnosis_data.get("total_time", 0.0),
                            diagnosis_data.get("status", "completed"),
                            now,
                        ),
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            conn.execute(
                """INSERT INTO diagnoses
                   (id, user_id, symptoms, age, gender, result_data,
                    specialist_routing, model_used, estimated_cost,
                    total_time, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    diag_id,
                    user_id,
                    encrypt(diagnosis_data.get("symptoms", "")),
                    diagnosis_data.get("age"),
                    diagnosis_data.get("gender"),
                    encrypt_json(diagnosis_data.get("result", {})),
                    json.dumps(diagnosis_data.get("specialist_routing", [])),
                    diagnosis_data.get("model_used", ""),
                    diagnosis_data.get("estimated_cost", 0.0),
                    diagnosis_data.get("total_time", 0.0),
                    diagnosis_data.get("status", "completed"),
                    now,
                ),
            )
            conn.commit()

        return {"id": diag_id, "user_id": user_id, "created_at": now}

    def get_user_diagnoses(self, user_id: str, page: int = 1,
                           limit: int = 20) -> dict:
        """Paginated list of a user's diagnoses (decrypted)."""
        offset = (page - 1) * limit

        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT COUNT(*) FROM diagnoses WHERE user_id = %s",
                        (user_id,),
                    )
                    total = cur.fetchone()[0]

                    cur.execute(
                        """SELECT * FROM diagnoses WHERE user_id = %s
                           ORDER BY created_at DESC LIMIT %s OFFSET %s""",
                        (user_id, limit, offset),
                    )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    rows = cur.fetchall()

                items = [self._pg_row_to_diagnosis(dict(zip(cols, r))) for r in rows]
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            total = conn.execute(
                "SELECT COUNT(*) FROM diagnoses WHERE user_id = ?", (user_id,)
            ).fetchone()[0]

            rows = conn.execute(
                """SELECT * FROM diagnoses WHERE user_id = ?
                   ORDER BY created_at DESC LIMIT ? OFFSET ?""",
                (user_id, limit, offset),
            ).fetchall()

            items = [self._sqlite_row_to_diagnosis(r) for r in rows]

        return {"items": items, "total": total, "page": page, "limit": limit}

    def get_diagnosis(self, diagnosis_id: str, user_id: str = None) -> Optional[dict]:
        """Get a single diagnosis, optionally with ownership check."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    if user_id:
                        cur.execute(
                            "SELECT * FROM diagnoses WHERE id = %s AND user_id = %s",
                            (diagnosis_id, user_id),
                        )
                    else:
                        cur.execute(
                            "SELECT * FROM diagnoses WHERE id = %s",
                            (diagnosis_id,),
                        )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    row = cur.fetchone()
                if row is None:
                    return None
                return self._pg_row_to_diagnosis(dict(zip(cols, row)))
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            if user_id:
                row = conn.execute(
                    "SELECT * FROM diagnoses WHERE id = ? AND user_id = ?",
                    (diagnosis_id, user_id),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT * FROM diagnoses WHERE id = ?",
                    (diagnosis_id,),
                ).fetchone()
            if row is None:
                return None
            return self._sqlite_row_to_diagnosis(row)

    # -- diagnosis row converters ------------------------------------------

    def _pg_row_to_diagnosis(self, row: dict) -> dict:
        result = None
        if row.get("result_encrypted"):
            result = decrypt_json(row["result_encrypted"])

        specialist = row.get("specialist_routing")
        if isinstance(specialist, str):
            try:
                specialist = json.loads(specialist)
            except (json.JSONDecodeError, TypeError):
                specialist = []
        elif specialist is None:
            specialist = []

        return {
            "id": str(row["id"]),
            "user_id": str(row["user_id"]),
            "symptoms": decrypt(row.get("symptoms_encrypted", "")) or "",
            "age": row.get("age"),
            "gender": row.get("gender"),
            "result_data": result,
            "specialist_routing": specialist,
            "model_used": row.get("model_used"),
            "estimated_cost": float(row["estimated_cost"]) if row.get("estimated_cost") else 0.0,
            "total_time": float(row["total_time"]) if row.get("total_time") else 0.0,
            "status": row.get("status", "completed"),
            "created_at": row["created_at"].isoformat() if hasattr(row["created_at"], "isoformat") else str(row["created_at"]),
        }

    def _sqlite_row_to_diagnosis(self, row: sqlite3.Row) -> dict:
        result = None
        if row["result_data"]:
            result = decrypt_json(row["result_data"])

        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "symptoms": decrypt(row["symptoms"]) if row["symptoms"] else "",
            "age": row["age"],
            "gender": row["gender"],
            "result_data": result,
            "specialist_routing": json.loads(row["specialist_routing"]) if row["specialist_routing"] else [],
            "model_used": row["model_used"],
            "estimated_cost": row["estimated_cost"],
            "total_time": row["total_time"],
            "status": row["status"],
            "created_at": row["created_at"],
        }

    # ======================================================================
    # AUDIT LOG
    # ======================================================================

    def log_audit(self, user_id: Optional[str], action: str,
                  resource: Optional[str] = None,
                  ip: Optional[str] = None,
                  details: Optional[dict] = None) -> None:
        """Write an audit trail entry."""
        now = datetime.now(timezone.utc).isoformat()

        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO audit_log
                           (user_id, action, resource_type, ip_address, timestamp, details)
                           VALUES (%s, %s, %s, %s::inet, %s, %s::jsonb)""",
                        (
                            user_id,
                            action,
                            resource,
                            ip if ip and ip != "unknown" else None,
                            now,
                            json.dumps(details) if details else None,
                        ),
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            conn.execute(
                """INSERT INTO audit_log (user_id, action, resource, ip_address, timestamp, details)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, action, resource, ip, now,
                 json.dumps(details) if details else None),
            )
            conn.commit()

    def get_audit_log(self, user_id: Optional[str] = None,
                      action: Optional[str] = None,
                      limit: int = 100, offset: int = 0) -> list:
        """Retrieve audit log entries with optional filters."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                clauses = []
                params = []
                if user_id:
                    clauses.append("user_id = %s")
                    params.append(user_id)
                if action:
                    clauses.append("action = %s")
                    params.append(action)

                where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
                params.extend([limit, offset])

                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT * FROM audit_log{where} ORDER BY timestamp DESC LIMIT %s OFFSET %s",
                        params,
                    )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    rows = cur.fetchall()

                return [
                    {
                        "id": r[cols.index("id")],
                        "user_id": str(r[cols.index("user_id")]) if r[cols.index("user_id")] else None,
                        "action": r[cols.index("action")],
                        "resource": r[cols.index("resource_type")],
                        "ip_address": str(r[cols.index("ip_address")]) if r[cols.index("ip_address")] else None,
                        "timestamp": r[cols.index("timestamp")].isoformat() if hasattr(r[cols.index("timestamp")], "isoformat") else str(r[cols.index("timestamp")]),
                        "details": r[cols.index("details")],
                    }
                    for r in rows
                ]
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            clauses = []
            params = []
            if user_id:
                clauses.append("user_id = ?")
                params.append(user_id)
            if action:
                clauses.append("action = ?")
                params.append(action)

            where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
            params.extend([limit, offset])

            rows = conn.execute(
                f"SELECT * FROM audit_log{where} ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                params,
            ).fetchall()

            return [
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "action": row["action"],
                    "resource": row["resource"],
                    "ip_address": row["ip_address"],
                    "timestamp": row["timestamp"],
                    "details": json.loads(row["details"]) if row["details"] else None,
                }
                for row in rows
            ]

    # ======================================================================
    # SESSION MANAGEMENT
    # ======================================================================

    def create_session(self, user_id: str, token_hash: str,
                       ip: Optional[str] = None,
                       user_agent: Optional[str] = None,
                       expires_at: Optional[str] = None) -> dict:
        """Store a hashed refresh token session."""
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        if expires_at is None:
            expires_at = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO sessions
                           (id, user_id, token_hash, created_at, expires_at,
                            ip_address, user_agent)
                           VALUES (%s, %s, %s, %s, %s, %s::inet, %s)""",
                        (session_id, user_id, token_hash, now, expires_at,
                         ip if ip and ip != "unknown" else None, user_agent),
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            conn.execute(
                """INSERT INTO sessions (id, user_id, token_hash, created_at,
                   expires_at, ip_address, user_agent)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (session_id, user_id, token_hash, now, expires_at, ip, user_agent),
            )
            conn.commit()

        return {"id": session_id, "user_id": user_id, "expires_at": expires_at}

    def revoke_session(self, session_id: str) -> None:
        """Revoke a single refresh token session."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE sessions SET is_revoked = TRUE, revoked_at = NOW() WHERE id = %s",
                        (session_id,),
                    )
                conn.commit()
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            conn.execute(
                "UPDATE sessions SET is_revoked = 1 WHERE id = ?", (session_id,)
            )
            conn.commit()

    def revoke_user_sessions(self, user_id: str) -> None:
        """Revoke all sessions for a user."""
        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE sessions SET is_revoked = TRUE, revoked_at = NOW() WHERE user_id = %s",
                        (user_id,),
                    )
                conn.commit()
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            conn.execute(
                "UPDATE sessions SET is_revoked = 1 WHERE user_id = ?", (user_id,)
            )
            conn.commit()

    # Alias for spec compatibility
    revoke_all_sessions = revoke_user_sessions

    def find_session_by_token_hash(self, token_hash: str) -> Optional[dict]:
        """Find an active (non-revoked, non-expired) session by token hash."""
        now = datetime.now(timezone.utc).isoformat()

        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT * FROM sessions
                           WHERE token_hash = %s AND is_revoked = FALSE
                           AND expires_at > %s""",
                        (token_hash, now),
                    )
                    cols = [d[0] for d in cur.description] if cur.description else []
                    row = cur.fetchone()
                if row is None:
                    return None
                rd = dict(zip(cols, row))
                return {k: (str(v) if hasattr(v, "hex") else v) for k, v in rd.items()}
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            row = conn.execute(
                """SELECT * FROM sessions
                   WHERE token_hash = ? AND is_revoked = 0
                   AND expires_at > ?""",
                (token_hash, now),
            ).fetchone()
            if row is None:
                return None
            return dict(row)

    # Alias for spec compatibility
    get_session_by_token = find_session_by_token_hash

    def cleanup_expired_sessions(self) -> int:
        """Remove expired or revoked sessions. Returns count deleted."""
        now = datetime.now(timezone.utc).isoformat()

        if self._use_pg:
            conn = self._pg_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM sessions WHERE expires_at < %s OR is_revoked = TRUE",
                        (now,),
                    )
                    count = cur.rowcount
                conn.commit()
                return count
            finally:
                self._pg_put(conn)
        else:
            conn = self._conn()
            cursor = conn.execute(
                "DELETE FROM sessions WHERE expires_at < ? OR is_revoked = 1",
                (now,),
            )
            conn.commit()
            return cursor.rowcount


# ---------------------------------------------------------------------------
# Proxy so external code calling db._conn().execute() works in PG mode
# ---------------------------------------------------------------------------

class _PgConnProxy:
    """Thin wrapper allowing db._conn().execute(sql, params) to work
    against PostgreSQL.  Translates ``?`` placeholders to ``%s`` and
    converts sqlite3-style calls into psycopg2 cursor operations.
    """

    def __init__(self, db: Database):
        self._db = db
        self._conn = db._pg_conn()

    def execute(self, sql: str, params=None):
        # Translate ? -> %s for sqlite-style queries
        sql = sql.replace("?", "%s")
        cur = self._conn.cursor()
        cur.execute(sql, params or ())
        return cur

    def commit(self):
        self._conn.commit()
        self._db._pg_put(self._conn)

    def rollback(self):
        self._conn.rollback()
        self._db._pg_put(self._conn)


# ---------------------------------------------------------------------------
# Module-level convenience
# ---------------------------------------------------------------------------

def get_db() -> Database:
    """Return the singleton Database instance."""
    return Database.get()
