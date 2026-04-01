"""
Authentication API routes.

POST /api/auth/signup          - Register new user
POST /api/auth/login           - Log in
POST /api/auth/refresh         - Refresh access token
POST /api/auth/logout          - Revoke refresh token
GET  /api/auth/me              - Current user profile
PUT  /api/auth/me              - Update profile
POST /api/auth/change-password - Change password
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, EmailStr, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address

from database import Database

limiter = Limiter(key_func=get_remote_address)
from auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    hash_token,
    hash_password,
    verify_password,
    get_current_user,
)

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str = ""

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Invalid email address")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    profile_data: Optional[dict] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _user_agent(request: Request) -> str:
    return request.headers.get("user-agent", "unknown")[:256]


def _safe_user(user: dict) -> dict:
    """Strip sensitive fields before sending to client."""
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user.get("name", ""),
        "role": user.get("role", "patient"),
        "created_at": user.get("created_at"),
        "profile_data": user.get("profile_data"),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@auth_router.post("/signup")
@limiter.limit("3/minute")
async def signup(body: SignupRequest, request: Request):
    """Register a new user account."""
    # Rate limiting placeholder — in production use Redis-based rate limiter
    # e.g. slowapi or fastapi-limiter: @limiter.limit("5/minute")

    db = Database.get()

    try:
        user = db.create_user(
            email=body.email,
            password=body.password,
            name=body.name,
            role="patient",
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    # Issue tokens
    access = create_access_token(user["id"], user["role"])
    refresh = create_refresh_token(user["id"])

    # Store hashed refresh token
    db.create_session(
        user_id=user["id"],
        token_hash=hash_token(refresh),
        ip=_client_ip(request),
        user_agent=_user_agent(request),
        expires_at=(datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
    )

    # Audit
    db.log_audit(user["id"], "signup", "user", _client_ip(request))

    return {
        "user": _safe_user(user),
        "access_token": access,
        "refresh_token": refresh,
    }


@auth_router.post("/login")
@limiter.limit("5/minute")
async def login(body: LoginRequest, request: Request):
    """Authenticate with email + password."""

    db = Database.get()
    user = db.authenticate(body.email, body.password)

    if user is None:
        # Constant-time-ish response to avoid timing attacks
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access = create_access_token(user["id"], user["role"])
    refresh = create_refresh_token(user["id"])

    db.create_session(
        user_id=user["id"],
        token_hash=hash_token(refresh),
        ip=_client_ip(request),
        user_agent=_user_agent(request),
        expires_at=(datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
    )

    db.log_audit(user["id"], "login", "user", _client_ip(request))

    return {
        "user": _safe_user(user),
        "access_token": access,
        "refresh_token": refresh,
    }


@auth_router.post("/refresh")
async def refresh(body: RefreshRequest, request: Request):
    """Exchange a valid refresh token for a new access token."""
    payload = verify_token(body.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    db = Database.get()
    th = hash_token(body.refresh_token)
    session = db.find_session_by_token_hash(th)
    if session is None:
        raise HTTPException(status_code=401, detail="Refresh token revoked or expired")

    user = db.get_user(payload["sub"])
    if user is None or not user.get("is_active"):
        raise HTTPException(status_code=401, detail="User not found")

    access = create_access_token(user["id"], user["role"])

    return {"access_token": access}


@auth_router.post("/logout")
async def logout(request: Request, user: dict = Depends(get_current_user)):
    """Revoke all refresh tokens for the current user."""
    db = Database.get()
    db.revoke_user_sessions(user["id"])
    db.log_audit(user["id"], "logout", "user", _client_ip(request))
    return {"message": "Logged out successfully"}


@auth_router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Return the current user's profile."""
    return {"user": _safe_user(user)}


@auth_router.put("/me")
async def update_me(body: ProfileUpdateRequest, request: Request,
                    user: dict = Depends(get_current_user)):
    """Update the current user's profile."""
    db = Database.get()
    updates = {}
    if body.name is not None:
        updates["name"] = body.name
    if body.profile_data is not None:
        updates["profile_data"] = body.profile_data

    if not updates:
        return {"user": _safe_user(user)}

    updated = db.update_user(user["id"], updates)
    db.log_audit(user["id"], "update_profile", "user", _client_ip(request))
    return {"user": _safe_user(updated)}


@auth_router.post("/change-password")
async def change_password(body: ChangePasswordRequest, request: Request,
                          user: dict = Depends(get_current_user)):
    """Change the current user's password."""
    db = Database.get()

    # Verify old password
    check = db.authenticate(user["email"], body.old_password)
    if check is None:
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Update password hash
    new_hash = hash_password(body.new_password)
    conn = db._conn()
    conn.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                 (new_hash, user["id"]))
    conn.commit()

    # Revoke all existing sessions (force re-login)
    db.revoke_user_sessions(user["id"])

    db.log_audit(user["id"], "change_password", "user", _client_ip(request))

    return {"message": "Password changed. Please log in again."}
