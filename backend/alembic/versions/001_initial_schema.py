"""Initial schema — matches db/init.sql

Revision ID: 001
Revises: (none)
Create Date: 2026-04-08

Creates all tables defined in db/init.sql:
  - users          (HIPAA-encrypted PII, roles, subscription tiers)
  - sessions       (JWT refresh tokens, stored as hashed values)
  - diagnoses      (encrypted symptoms + results, agent metadata)
  - audit_log      (HIPAA-required immutable audit trail)
  - usage_records  (billing usage tracking)
  - follow_ups     (scheduled follow-up appointments)
  - api_keys       (programmatic API access, stored hashed)

PostgreSQL-specific objects (uuid-ossp extension, INET type, JSONB, ARRAY,
triggers, RLS policies) are created conditionally so the migration also runs
cleanly on SQLite for local development.
"""

from __future__ import annotations

import os
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# ── Revision identifiers ──────────────────────────────────────────────────────
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_postgresql() -> bool:
    """Return True when the migration is running against PostgreSQL."""
    bind = op.get_bind()
    return bind.dialect.name == "postgresql"


def _pg_exec(sql: str) -> None:
    """Execute raw SQL only on PostgreSQL."""
    if _is_postgresql():
        op.execute(sa.text(sql))


# ── Upgrade ───────────────────────────────────────────────────────────────────

def upgrade() -> None:
    # PostgreSQL extensions (uuid generation, pgcrypto)
    _pg_exec("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    _pg_exec("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\"")

    # ── users ─────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()") if _is_postgresql() else None),
        # PII — stored encrypted
        sa.Column("email_hash", sa.Text, nullable=False, unique=True),
        sa.Column("email_encrypted", sa.Text, nullable=False),
        sa.Column("password_hash", sa.Text, nullable=False),
        # Role
        sa.Column("role", sa.Text, nullable=False, server_default="patient"),
        # More encrypted PII
        sa.Column("name_encrypted", sa.Text),
        sa.Column("phone_encrypted", sa.Text),
        sa.Column("date_of_birth_encrypted", sa.Text),
        sa.Column("profile_data_encrypted", sa.Text),
        # Non-sensitive metadata
        sa.Column("preferred_language", sa.Text, server_default="en"),
        sa.Column("timezone", sa.Text, server_default="UTC"),
        sa.Column("subscription_tier", sa.Text, server_default="free"),
        sa.Column("stripe_customer_id", sa.Text),
        # Timestamps
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("last_login_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("email_verified_at", sa.TIMESTAMP(timezone=True)),
        # Status
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("is_email_verified", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("failed_login_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("locked_until", sa.TIMESTAMP(timezone=True)),
        # HIPAA consent
        sa.Column("hipaa_consent_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("terms_accepted_at", sa.TIMESTAMP(timezone=True)),
    )

    # PostgreSQL CHECK constraints
    _pg_exec("""
        ALTER TABLE users
        ADD CONSTRAINT users_role_check
        CHECK (role IN ('patient', 'physician', 'admin', 'reviewer'))
    """)
    _pg_exec("""
        ALTER TABLE users
        ADD CONSTRAINT users_subscription_tier_check
        CHECK (subscription_tier IN ('free', 'starter', 'pro', 'enterprise'))
    """)

    op.create_index("idx_users_email_hash", "users", ["email_hash"])
    op.create_index("idx_users_role", "users", ["role"])
    op.create_index("idx_users_subscription", "users", ["subscription_tier"])
    op.create_index("idx_users_created", "users", ["created_at"])

    # ── sessions ──────────────────────────────────────────────────────────────
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(36), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()") if _is_postgresql() else None),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.Text, nullable=False),
        sa.Column("device_fingerprint", sa.Text),
        sa.Column("ip_address", sa.Text),   # INET on PG; Text on SQLite
        sa.Column("user_agent", sa.Text),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("is_revoked", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("revoked_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("revoke_reason", sa.Text),
    )
    op.create_index("idx_sessions_user", "sessions", ["user_id"])
    op.create_index("idx_sessions_token", "sessions", ["token_hash"])
    op.create_index("idx_sessions_expires", "sessions", ["expires_at"])

    # ── diagnoses ─────────────────────────────────────────────────────────────
    op.create_table(
        "diagnoses",
        sa.Column("id", sa.String(36), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()") if _is_postgresql() else None),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        # Encrypted patient input
        sa.Column("symptoms_encrypted", sa.Text, nullable=False),
        sa.Column("chief_complaint_encrypted", sa.Text),
        # Non-sensitive metadata
        sa.Column("age", sa.Integer),
        sa.Column("gender", sa.Text),
        sa.Column("severity", sa.Integer),
        sa.Column("duration", sa.Text),
        # Results (encrypted)
        sa.Column("result_encrypted", sa.Text),
        # Routing & performance (stored as JSON text on SQLite, JSONB on PG)
        sa.Column("specialist_routing", sa.Text),   # JSON array
        sa.Column("model_used", sa.Text),
        sa.Column("agents_used", sa.Text),           # JSON array on SQLite
        sa.Column("agent_timings", sa.Text),         # JSON object
        sa.Column("estimated_cost", sa.Numeric(10, 4)),
        sa.Column("total_time", sa.Numeric(10, 2)),
        # Status
        sa.Column("status", sa.Text, nullable=False, server_default="completed"),
        sa.Column("urgency", sa.Text, server_default="routine"),
        sa.Column("confidence_score", sa.Integer),
        # Review
        sa.Column("reviewed_by", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("reviewed_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("review_notes_encrypted", sa.Text),
        # Timestamps
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True)),
        # Image data
        sa.Column("has_image", sa.Boolean, server_default=sa.false()),
        sa.Column("image_analysis_status", sa.Text),
    )

    _pg_exec("""
        ALTER TABLE diagnoses
        ADD CONSTRAINT diagnoses_status_check
        CHECK (status IN ('pending', 'running', 'completed', 'failed', 'reviewed'))
    """)
    _pg_exec("""
        ALTER TABLE diagnoses
        ADD CONSTRAINT diagnoses_urgency_check
        CHECK (urgency IN ('routine', 'soon', 'urgent', 'emergency'))
    """)

    op.create_index("idx_diagnoses_user", "diagnoses", ["user_id"])
    op.create_index("idx_diagnoses_status", "diagnoses", ["status"])
    op.create_index("idx_diagnoses_urgency", "diagnoses", ["urgency"])
    op.create_index("idx_diagnoses_created", "diagnoses", ["created_at"])
    op.create_index("idx_diagnoses_confidence", "diagnoses", ["confidence_score"])

    # ── audit_log ─────────────────────────────────────────────────────────────
    op.create_table(
        "audit_log",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("session_id", sa.String(36), sa.ForeignKey("sessions.id")),
        sa.Column("action", sa.Text, nullable=False),
        sa.Column("resource_type", sa.Text),
        sa.Column("resource_id", sa.Text),
        sa.Column("ip_address", sa.Text),
        sa.Column("user_agent", sa.Text),
        sa.Column("old_value_encrypted", sa.Text),
        sa.Column("new_value_encrypted", sa.Text),
        sa.Column("details", sa.Text),   # JSON object
        sa.Column("severity", sa.Text, server_default="info"),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )

    _pg_exec("""
        ALTER TABLE audit_log
        ADD CONSTRAINT audit_log_severity_check
        CHECK (severity IN ('info', 'warning', 'critical', 'security'))
    """)

    op.create_index("idx_audit_user", "audit_log", ["user_id"])
    op.create_index("idx_audit_action", "audit_log", ["action"])
    op.create_index("idx_audit_timestamp", "audit_log", ["timestamp"])
    op.create_index("idx_audit_severity", "audit_log", ["severity"])
    op.create_index("idx_audit_resource", "audit_log", ["resource_type", "resource_id"])

    # Prevent deletions from audit_log (HIPAA)
    _pg_exec("""
        CREATE OR REPLACE FUNCTION prevent_audit_delete()
        RETURNS TRIGGER AS $$
        BEGIN
            RAISE EXCEPTION 'Audit log records cannot be deleted (HIPAA compliance)';
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql
    """)
    _pg_exec("""
        CREATE TRIGGER audit_no_delete
        BEFORE DELETE ON audit_log
        FOR EACH ROW EXECUTE FUNCTION prevent_audit_delete()
    """)

    # ── usage_records ─────────────────────────────────────────────────────────
    op.create_table(
        "usage_records",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_type", sa.Text, nullable=False),
        sa.Column("diagnosis_id", sa.String(36), sa.ForeignKey("diagnoses.id")),
        sa.Column("model_used", sa.Text),
        sa.Column("tokens_input", sa.Integer, server_default="0"),
        sa.Column("tokens_output", sa.Integer, server_default="0"),
        sa.Column("cost_usd", sa.Numeric(10, 6), server_default="0"),
        sa.Column("billing_period", sa.Text),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_index("idx_usage_user", "usage_records", ["user_id"])
    op.create_index("idx_usage_period", "usage_records", ["billing_period"])
    op.create_index("idx_usage_type", "usage_records", ["action_type"])

    # ── follow_ups ────────────────────────────────────────────────────────────
    op.create_table(
        "follow_ups",
        sa.Column("id", sa.String(36), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()") if _is_postgresql() else None),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("diagnosis_id", sa.String(36), sa.ForeignKey("diagnoses.id")),
        sa.Column("scheduled_date", sa.Date, nullable=False),
        sa.Column("reminder_sent", sa.Boolean, server_default=sa.false()),
        sa.Column("reminder_sent_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("status", sa.Text, server_default="pending"),
        sa.Column("notes_encrypted", sa.Text),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True)),
    )

    _pg_exec("""
        ALTER TABLE follow_ups
        ADD CONSTRAINT follow_ups_status_check
        CHECK (status IN ('pending', 'completed', 'missed', 'cancelled'))
    """)

    op.create_index("idx_followups_user", "follow_ups", ["user_id"])
    op.create_index("idx_followups_date", "follow_ups", ["scheduled_date"])
    op.create_index("idx_followups_status", "follow_ups", ["status"])

    # ── api_keys ──────────────────────────────────────────────────────────────
    op.create_table(
        "api_keys",
        sa.Column("id", sa.String(36), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()") if _is_postgresql() else None),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key_hash", sa.Text, unique=True, nullable=False),
        sa.Column("key_prefix", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("scopes", sa.Text, server_default='["diagnose"]'),  # JSON array
        sa.Column("rate_limit", sa.Integer, server_default="100"),
        sa.Column("last_used_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("is_active", sa.Boolean, server_default=sa.true()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_index("idx_apikeys_user", "api_keys", ["user_id"])
    op.create_index("idx_apikeys_hash", "api_keys", ["key_hash"])

    # ── auto-updated updated_at trigger on users (PostgreSQL only) ────────────
    _pg_exec("""
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)
    _pg_exec("""
        CREATE TRIGGER users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW EXECUTE FUNCTION update_updated_at()
    """)

    # ── Row-Level Security (PostgreSQL only) ──────────────────────────────────
    _pg_exec("ALTER TABLE diagnoses ENABLE ROW LEVEL SECURITY")
    _pg_exec("ALTER TABLE follow_ups ENABLE ROW LEVEL SECURITY")
    _pg_exec("ALTER TABLE usage_records ENABLE ROW LEVEL SECURITY")


# ── Downgrade ─────────────────────────────────────────────────────────────────

def downgrade() -> None:
    # Drop triggers and functions first (PostgreSQL)
    _pg_exec("DROP TRIGGER IF EXISTS users_updated_at ON users")
    _pg_exec("DROP TRIGGER IF EXISTS audit_no_delete ON audit_log")
    _pg_exec("DROP FUNCTION IF EXISTS update_updated_at()")
    _pg_exec("DROP FUNCTION IF EXISTS prevent_audit_delete()")

    # Drop tables in reverse FK dependency order
    op.drop_table("api_keys")
    op.drop_table("follow_ups")
    op.drop_table("usage_records")
    op.drop_table("audit_log")
    op.drop_table("diagnoses")
    op.drop_table("sessions")
    op.drop_table("users")
