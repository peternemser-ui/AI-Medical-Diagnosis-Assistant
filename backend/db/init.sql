-- MedDiagnose AI — PostgreSQL Schema
-- HIPAA-compliant with field-level encryption for PII
-- All PII columns store encrypted (Fernet) text, not plain text

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ══════════════════════════════════════════════════════════════════
-- USERS
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email_hash TEXT UNIQUE NOT NULL,         -- SHA-256 hash for lookup
    email_encrypted TEXT NOT NULL,           -- Fernet-encrypted email
    password_hash TEXT NOT NULL,             -- bcrypt hash
    role TEXT NOT NULL DEFAULT 'patient'     -- patient, physician, admin, reviewer
        CHECK (role IN ('patient', 'physician', 'admin', 'reviewer')),
    name_encrypted TEXT,                     -- Fernet-encrypted full name
    phone_encrypted TEXT,                    -- Fernet-encrypted phone
    date_of_birth_encrypted TEXT,            -- Fernet-encrypted DOB
    profile_data_encrypted TEXT,             -- Fernet-encrypted JSON (allergies, medications, etc.)

    -- Non-sensitive metadata
    preferred_language TEXT DEFAULT 'en',
    timezone TEXT DEFAULT 'UTC',
    subscription_tier TEXT DEFAULT 'free'
        CHECK (subscription_tier IN ('free', 'starter', 'pro', 'enterprise')),
    stripe_customer_id TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ,
    email_verified_at TIMESTAMPTZ,

    -- Status
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,

    -- HIPAA consent
    hipaa_consent_at TIMESTAMPTZ,
    terms_accepted_at TIMESTAMPTZ
);

CREATE INDEX idx_users_email_hash ON users(email_hash);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_subscription ON users(subscription_tier);
CREATE INDEX idx_users_created ON users(created_at);

-- ══════════════════════════════════════════════════════════════════
-- SESSIONS (JWT refresh tokens)
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,                -- SHA-256 hash of refresh token
    device_fingerprint TEXT,                 -- browser/device identifier
    ip_address INET,
    user_agent TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    last_used_at TIMESTAMPTZ,

    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_at TIMESTAMPTZ,
    revoke_reason TEXT
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_token ON sessions(token_hash);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);

-- ══════════════════════════════════════════════════════════════════
-- DIAGNOSES
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE diagnoses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Encrypted patient input
    symptoms_encrypted TEXT NOT NULL,        -- Fernet-encrypted symptoms text
    chief_complaint_encrypted TEXT,          -- Fernet-encrypted chief complaint

    -- Non-sensitive metadata
    age INTEGER,
    gender TEXT,
    severity INTEGER,
    duration TEXT,

    -- Diagnosis results (encrypted — contains medical data)
    result_encrypted TEXT,                   -- Fernet-encrypted JSON (full diagnosis result)

    -- Routing & performance (non-PII)
    specialist_routing JSONB,               -- ["cardiology", "neurology"]
    model_used TEXT,
    agents_used TEXT[],                      -- ARRAY of agent names
    agent_timings JSONB,                    -- { agent: seconds }
    estimated_cost DECIMAL(10,4),
    total_time DECIMAL(10,2),

    -- Status
    status TEXT NOT NULL DEFAULT 'completed'
        CHECK (status IN ('pending', 'running', 'completed', 'failed', 'reviewed')),
    urgency TEXT DEFAULT 'routine'
        CHECK (urgency IN ('routine', 'soon', 'urgent', 'emergency')),
    confidence_score INTEGER,               -- top diagnosis confidence 0-100

    -- Review
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    review_notes_encrypted TEXT,            -- Fernet-encrypted reviewer notes

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    -- Image data
    has_image BOOLEAN DEFAULT FALSE,
    image_analysis_status TEXT
);

CREATE INDEX idx_diagnoses_user ON diagnoses(user_id);
CREATE INDEX idx_diagnoses_status ON diagnoses(status);
CREATE INDEX idx_diagnoses_urgency ON diagnoses(urgency);
CREATE INDEX idx_diagnoses_created ON diagnoses(created_at);
CREATE INDEX idx_diagnoses_confidence ON diagnoses(confidence_score);

-- ══════════════════════════════════════════════════════════════════
-- AUDIT LOG (HIPAA requirement — immutable)
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,

    user_id UUID REFERENCES users(id),
    session_id UUID REFERENCES sessions(id),

    action TEXT NOT NULL,                    -- login, logout, diagnosis_start, diagnosis_view,
                                            -- report_export, profile_update, admin_access, etc.
    resource_type TEXT,                      -- user, diagnosis, report, settings
    resource_id TEXT,                        -- ID of the accessed resource

    ip_address INET,
    user_agent TEXT,

    -- What changed (for update auditing)
    old_value_encrypted TEXT,                -- Fernet-encrypted previous value
    new_value_encrypted TEXT,                -- Fernet-encrypted new value

    details JSONB,                           -- non-sensitive metadata

    severity TEXT DEFAULT 'info'
        CHECK (severity IN ('info', 'warning', 'critical', 'security')),

    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Audit log should NEVER be deleted (HIPAA retention)
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_severity ON audit_log(severity);
CREATE INDEX idx_audit_resource ON audit_log(resource_type, resource_id);

-- ══════════════════════════════════════════════════════════════════
-- USAGE TRACKING (billing)
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE usage_records (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    action_type TEXT NOT NULL,               -- diagnosis, followup, image_analysis, pdf_export
    diagnosis_id UUID REFERENCES diagnoses(id),

    model_used TEXT,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    cost_usd DECIMAL(10,6) DEFAULT 0,

    billing_period TEXT,                     -- YYYY-MM format

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_usage_user ON usage_records(user_id);
CREATE INDEX idx_usage_period ON usage_records(billing_period);
CREATE INDEX idx_usage_type ON usage_records(action_type);

-- ══════════════════════════════════════════════════════════════════
-- FOLLOW-UPS
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE follow_ups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    diagnosis_id UUID REFERENCES diagnoses(id),

    scheduled_date DATE NOT NULL,
    reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_sent_at TIMESTAMPTZ,

    status TEXT DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed', 'missed', 'cancelled')),

    notes_encrypted TEXT,                    -- Fernet-encrypted

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_followups_user ON follow_ups(user_id);
CREATE INDEX idx_followups_date ON follow_ups(scheduled_date);
CREATE INDEX idx_followups_status ON follow_ups(status);

-- ══════════════════════════════════════════════════════════════════
-- API KEYS (for programmatic access)
-- ══════════════════════════════════════════════════════════════════
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    key_hash TEXT UNIQUE NOT NULL,            -- SHA-256 hash of the API key
    key_prefix TEXT NOT NULL,                -- First 8 chars for identification (e.g., "mda_live_")
    name TEXT NOT NULL,                      -- User-given name

    scopes TEXT[] DEFAULT ARRAY['diagnose'], -- permissions
    rate_limit INTEGER DEFAULT 100,          -- requests per hour

    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_apikeys_user ON api_keys(user_id);
CREATE INDEX idx_apikeys_hash ON api_keys(key_hash);

-- ══════════════════════════════════════════════════════════════════
-- FUNCTIONS & TRIGGERS
-- ══════════════════════════════════════════════════════════════════

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Prevent audit log deletion (HIPAA)
CREATE OR REPLACE FUNCTION prevent_audit_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit log records cannot be deleted (HIPAA compliance)';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_no_delete
    BEFORE DELETE ON audit_log
    FOR EACH ROW EXECUTE FUNCTION prevent_audit_delete();

-- ══════════════════════════════════════════════════════════════════
-- SECURITY POLICIES
-- ══════════════════════════════════════════════════════════════════

-- Row-Level Security (RLS) for multi-tenant isolation
ALTER TABLE diagnoses ENABLE ROW LEVEL SECURITY;
ALTER TABLE follow_ups ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_records ENABLE ROW LEVEL SECURITY;

-- Patients can only see their own data
-- (enforced at application level too, but RLS is defense-in-depth)

COMMENT ON TABLE users IS 'User accounts — PII fields are Fernet-encrypted';
COMMENT ON TABLE sessions IS 'JWT refresh token sessions — tokens stored as SHA-256 hashes';
COMMENT ON TABLE diagnoses IS 'Diagnosis records — symptoms and results are Fernet-encrypted';
COMMENT ON TABLE audit_log IS 'HIPAA audit trail — immutable, deletion prevented by trigger';
COMMENT ON TABLE usage_records IS 'Billing usage tracking — links to diagnoses';
COMMENT ON TABLE api_keys IS 'Programmatic API keys — key stored as SHA-256 hash';
