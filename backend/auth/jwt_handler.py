"""JWT token handling for authentication."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

try:
    from jose import JWTError, jwt
except ImportError:
    # Fallback for environments without python-jose
    jwt = None
    JWTError = Exception

from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a new JWT access token.

    Args:
        data: The data to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    if jwt:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    else:
        # Simple fallback (not secure, for development only)
        import base64
        import json
        return base64.b64encode(json.dumps(to_encode).encode()).decode()


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a new JWT refresh token.

    Args:
        data: The data to encode in the token

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    if jwt:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    else:
        import base64
        import json
        return base64.b64encode(json.dumps(to_encode).encode()).decode()


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token to verify

    Returns:
        Decoded token payload or None if invalid
    """
    try:
        if jwt:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        else:
            # Simple fallback
            import base64
            import json
            payload = json.loads(base64.b64decode(token).decode())
            # Check expiration
            if datetime.fromisoformat(payload.get("exp", "1970-01-01")) < datetime.utcnow():
                return None
            return payload
    except (JWTError, Exception):
        return None


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token without verification (for debugging).

    Args:
        token: The JWT token to decode

    Returns:
        Decoded token payload or None if invalid format
    """
    try:
        if jwt:
            # Decode without verification
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        else:
            import base64
            import json
            return json.loads(base64.b64decode(token).decode())
    except Exception:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired.

    Args:
        token: The JWT token to check

    Returns:
        True if expired, False otherwise
    """
    payload = decode_token(token)
    if not payload:
        return True

    exp = payload.get("exp")
    if not exp:
        return True

    if isinstance(exp, (int, float)):
        return datetime.fromtimestamp(exp) < datetime.utcnow()

    return True


def get_token_expiry(token: str) -> Optional[datetime]:
    """
    Get the expiration datetime of a token.

    Args:
        token: The JWT token

    Returns:
        Expiration datetime or None
    """
    payload = decode_token(token)
    if not payload:
        return None

    exp = payload.get("exp")
    if isinstance(exp, (int, float)):
        return datetime.fromtimestamp(exp)

    return None
