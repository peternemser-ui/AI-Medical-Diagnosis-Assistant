import hashlib
import secrets
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import base64
import json
import os

# In production, use proper libraries like passlib and python-jose
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt.

    In production, use bcrypt or argon2 via passlib.
    """
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return f"{salt}:{password_hash}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, stored_hash = hashed_password.split(":")
        password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        return hmac.compare_digest(password_hash, stored_hash)
    except ValueError:
        return False


def create_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT-like token.

    In production, use python-jose for proper JWT handling.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.isoformat(), "iat": datetime.utcnow().isoformat()})

    # Create token
    payload = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode()
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return f"{payload}.{signature}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a token."""
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None

        payload_b64, signature = parts

        # Verify signature
        expected_sig = hmac.new(
            SECRET_KEY.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return None

        # Decode payload
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())

        # Check expiration
        exp = datetime.fromisoformat(payload.get("exp", ""))
        if exp < datetime.utcnow():
            return None

        return payload
    except Exception:
        return None


def generate_verification_token() -> str:
    """Generate a random verification token."""
    return secrets.token_urlsafe(32)


def generate_reset_token() -> str:
    """Generate a random password reset token."""
    return secrets.token_urlsafe(32)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password meets security requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    if not has_lower:
        return False, "Password must contain at least one lowercase letter"
    if not has_digit:
        return False, "Password must contain at least one digit"
    if not has_special:
        return False, "Password must contain at least one special character"

    return True, "Password meets requirements"


def sanitize_email(email: str) -> str:
    """Sanitize and normalize email address."""
    return email.lower().strip()


def mask_email(email: str) -> str:
    """Mask email for privacy (e.g., j***@example.com)."""
    try:
        local, domain = email.split("@")
        if len(local) <= 2:
            masked_local = local[0] + "*" * (len(local) - 1)
        else:
            masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
        return f"{masked_local}@{domain}"
    except ValueError:
        return "***@***"
