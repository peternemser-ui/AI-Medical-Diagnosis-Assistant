"""FastAPI authentication dependencies."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import verify_token

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


async def get_token(
    oauth2_token: Optional[str] = Depends(oauth2_scheme),
    bearer_token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> Optional[str]:
    """
    Extract token from request headers.

    Supports both OAuth2 and Bearer token formats.
    """
    if oauth2_token:
        return oauth2_token
    if bearer_token:
        return bearer_token.credentials
    return None


async def get_current_user(token: Optional[str] = Depends(get_token)) -> dict:
    """
    Get the current authenticated user from the JWT token.

    Args:
        token: JWT token from request

    Returns:
        User data dictionary

    Raises:
        HTTPException: If token is invalid or missing
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # In a real application, you would fetch the user from the database
    user = {
        "id": user_id,
        "email": payload.get("email"),
        "name": payload.get("name"),
        "is_active": payload.get("is_active", True),
        "is_admin": payload.get("is_admin", False)
    }

    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get the current active user.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        User data dictionary if active

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(current_user: dict = Depends(get_current_active_user)) -> dict:
    """
    Get the current admin user.

    Args:
        current_user: User from get_current_active_user dependency

    Returns:
        User data dictionary if admin

    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


async def get_optional_user(token: Optional[str] = Depends(get_token)) -> Optional[dict]:
    """
    Get the current user if authenticated, None otherwise.

    This dependency doesn't raise an exception for missing/invalid tokens.

    Args:
        token: JWT token from request

    Returns:
        User data dictionary or None
    """
    if not token:
        return None

    payload = verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    return {
        "id": user_id,
        "email": payload.get("email"),
        "name": payload.get("name"),
        "is_active": payload.get("is_active", True),
        "is_admin": payload.get("is_admin", False)
    }
