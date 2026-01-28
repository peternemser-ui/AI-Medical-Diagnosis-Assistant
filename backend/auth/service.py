from datetime import datetime, timedelta
from typing import Optional, List
import uuid

from .models import (
    UserCreate, User, UserUpdate, UserInDB, Session,
    PasswordReset, AuthResponse, TokenResponse
)
from .utils import hash_password, verify_password, create_token, verify_token


class AuthService:
    """Authentication service handling user management and sessions."""

    def __init__(self):
        # In production, these would be database collections
        self._users: dict[str, UserInDB] = {}
        self._sessions: dict[str, Session] = {}
        self._password_resets: dict[str, PasswordReset] = {}
        self._email_verifications: dict[str, str] = {}

    async def register(self, user_data: UserCreate) -> AuthResponse:
        """Register a new user."""
        # Check if email already exists
        for user in self._users.values():
            if user.email == user_data.email:
                raise ValueError("Email already registered")

        user_id = str(uuid.uuid4())
        now = datetime.utcnow()

        user_in_db = UserInDB(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            role=user_data.role,
            hashed_password=hash_password(user_data.password),
            created_at=now,
            updated_at=now
        )

        self._users[user_id] = user_in_db

        # Create session and token
        token = create_token({"sub": user_id, "email": user_data.email})
        await self._create_session(user_id, token)

        # Send verification email (async task in production)
        await self._send_verification_email(user_data.email)

        user = User(**user_in_db.model_dump(exclude={"hashed_password"}))
        return AuthResponse(token=token, user=user)

    async def login(
        self,
        email: str,
        password: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuthResponse:
        """Authenticate user and create session."""
        user_in_db = await self._get_user_by_email(email)

        if not user_in_db:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user_in_db.hashed_password):
            raise ValueError("Invalid credentials")

        if not user_in_db.is_active:
            raise ValueError("Account is disabled")

        # Create token and session
        token = create_token({"sub": user_in_db.id, "email": email})
        await self._create_session(
            user_in_db.id,
            token,
            device_info=device_info,
            ip_address=ip_address
        )

        user = User(**user_in_db.model_dump(exclude={"hashed_password"}))
        return AuthResponse(token=token, user=user)

    async def logout(self, user_id: str) -> None:
        """Logout user and invalidate current session."""
        sessions_to_remove = [
            sid for sid, session in self._sessions.items()
            if session.user_id == user_id and session.is_active
        ]
        for sid in sessions_to_remove:
            self._sessions[sid].is_active = False

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        user_in_db = self._users.get(user_id)
        if user_in_db:
            return User(**user_in_db.model_dump(exclude={"hashed_password"}))
        return None

    async def _get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email (internal)."""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def update_profile(self, user_id: str, profile_data: UserUpdate) -> User:
        """Update user profile."""
        user_in_db = self._users.get(user_id)
        if not user_in_db:
            raise ValueError("User not found")

        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_in_db, field, value)

        user_in_db.updated_at = datetime.utcnow()
        self._users[user_id] = user_in_db

        return User(**user_in_db.model_dump(exclude={"hashed_password"}))

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> None:
        """Change user password."""
        user_in_db = self._users.get(user_id)
        if not user_in_db:
            raise ValueError("User not found")

        if not verify_password(current_password, user_in_db.hashed_password):
            raise ValueError("Current password is incorrect")

        user_in_db.hashed_password = hash_password(new_password)
        user_in_db.updated_at = datetime.utcnow()
        self._users[user_id] = user_in_db

    async def request_password_reset(self, email: str) -> None:
        """Request password reset."""
        user = await self._get_user_by_email(email)
        if not user:
            return  # Don't reveal if email exists

        reset_id = str(uuid.uuid4())
        token = str(uuid.uuid4())
        now = datetime.utcnow()

        reset = PasswordReset(
            id=reset_id,
            user_id=user.id,
            token=token,
            created_at=now,
            expires_at=now + timedelta(hours=1)
        )

        self._password_resets[reset_id] = reset

        # Send reset email (async task in production)
        await self._send_password_reset_email(email, token)

    async def reset_password(self, token: str, new_password: str) -> None:
        """Reset password using token."""
        reset = None
        for r in self._password_resets.values():
            if r.token == token and not r.used:
                reset = r
                break

        if not reset:
            raise ValueError("Invalid or expired reset token")

        if reset.expires_at < datetime.utcnow():
            raise ValueError("Reset token has expired")

        user_in_db = self._users.get(reset.user_id)
        if not user_in_db:
            raise ValueError("User not found")

        user_in_db.hashed_password = hash_password(new_password)
        user_in_db.updated_at = datetime.utcnow()
        self._users[reset.user_id] = user_in_db

        reset.used = True

    async def verify_email(self, token: str) -> None:
        """Verify user email."""
        user_id = self._email_verifications.get(token)
        if not user_id:
            raise ValueError("Invalid verification token")

        user_in_db = self._users.get(user_id)
        if user_in_db:
            user_in_db.email_verified = True
            user_in_db.updated_at = datetime.utcnow()
            self._users[user_id] = user_in_db

        del self._email_verifications[token]

    async def resend_verification(self, email: str) -> None:
        """Resend verification email."""
        user = await self._get_user_by_email(email)
        if user and not user.email_verified:
            await self._send_verification_email(email)

    async def refresh_token(self, user_id: str) -> TokenResponse:
        """Refresh access token."""
        user = self._users.get(user_id)
        if not user:
            raise ValueError("User not found")

        access_token = create_token(
            {"sub": user_id, "email": user.email},
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_token(
            {"sub": user_id, "type": "refresh"},
            expires_delta=timedelta(days=7)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900
        )

    async def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get all active sessions for user."""
        return [
            session for session in self._sessions.values()
            if session.user_id == user_id and session.is_active
        ]

    async def revoke_session(self, user_id: str, session_id: str) -> None:
        """Revoke a specific session."""
        session = self._sessions.get(session_id)
        if session and session.user_id == user_id:
            session.is_active = False

    async def revoke_all_sessions(self, user_id: str) -> None:
        """Revoke all sessions for user."""
        for session in self._sessions.values():
            if session.user_id == user_id:
                session.is_active = False

    async def _create_session(
        self,
        user_id: str,
        token: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Session:
        """Create new session."""
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()

        session = Session(
            id=session_id,
            user_id=user_id,
            token=token,
            device_info=device_info,
            ip_address=ip_address,
            created_at=now,
            expires_at=now + timedelta(days=30)
        )

        self._sessions[session_id] = session
        return session

    async def _send_verification_email(self, email: str) -> None:
        """Send email verification (stub)."""
        # In production, integrate with email service
        pass

    async def _send_password_reset_email(self, email: str, token: str) -> None:
        """Send password reset email (stub)."""
        # In production, integrate with email service
        pass
