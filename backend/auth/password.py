"""Password hashing and verification utilities."""

import os
import hashlib
import secrets
from typing import Tuple

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_PASSLIB = True
except ImportError:
    pwd_context = None
    USE_PASSLIB = False


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt or fallback to SHA-256.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    if USE_PASSLIB and pwd_context:
        return pwd_context.hash(password)
    else:
        # Fallback using hashlib (less secure, for development)
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password

    Returns:
        True if password matches, False otherwise
    """
    if USE_PASSLIB and pwd_context:
        return pwd_context.verify(plain_password, hashed_password)
    else:
        # Fallback verification
        try:
            salt, stored_hash = hashed_password.split("$")
            computed_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
            return secrets.compare_digest(computed_hash, stored_hash)
        except (ValueError, AttributeError):
            return False


def generate_password_reset_token() -> str:
    """
    Generate a secure password reset token.

    Returns:
        Random token string
    """
    return secrets.token_urlsafe(32)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password meets strength requirements.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"

    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Password must contain at least one special character"

    return True, ""


def generate_temp_password(length: int = 12) -> str:
    """
    Generate a temporary password.

    Args:
        length: Desired password length

    Returns:
        Random temporary password
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
