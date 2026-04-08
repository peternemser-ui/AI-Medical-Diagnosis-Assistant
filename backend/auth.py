"""
JWT authentication with refresh tokens for HIPAA-compliant session management.

Access tokens: 15-minute expiry, contain user_id + role (no PII).
Refresh tokens: 7-day expiry, stored hashed in the sessions table.
"""

import os
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
import bcrypt
from fastapi import Request, HTTPException
from dotenv import load_dotenv

from database import Database, _append_env

load_dotenv()

# ---------------------------------------------------------------------------
# Key management
# ---------------------------------------------------------------------------

_JWT_ALGORITHM = "HS256"
_ACCESS_TOKEN_MINUTES = 15
_REFRESH_TOKEN_DAYS = 7


def _get_jwt_secret() -> str:
    """Load JWT secret from env or generate and persist one."""
    secret = os.getenv("JWT_SECRET")
    if secret:
        return secret

    import secrets
    new_secret = secrets.token_urlsafe(64)
    _append_env("JWT_SECRET", new_secret)
    os.environ["JWT_SECRET"] = new_secret
    return new_secret


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ---------------------------------------------------------------------------
# Token creation & verification
# ---------------------------------------------------------------------------

def create_access_token(user_id: str, role: str) -> str:
    """Create a short-lived JWT access token (15 min). No PII in payload."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=_ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=_JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a long-lived JWT refresh token (7 days)."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=_REFRESH_TOKEN_DAYS),
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=_JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(token, _get_jwt_secret(), algorithms=[_JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def hash_token(token: str) -> str:
    """SHA-256 hash of a token for secure DB storage."""
    return hashlib.sha256(token.encode()).hexdigest()


# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------

async def get_current_user(request: Request) -> dict:
    """FastAPI dependency: extract and verify user from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ", 1)[1]
    payload = verify_token(token)

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    db = Database.get()
    user = db.get_user(payload["sub"])
    if user is None or not user.get("is_active"):
        raise HTTPException(status_code=401, detail="User not found or deactivated")

    return user


async def get_optional_user(request: Request) -> Optional[dict]:
    """FastAPI dependency: extract user if token present, else None."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    try:
        return await get_current_user(request)
    except HTTPException:
        return None
