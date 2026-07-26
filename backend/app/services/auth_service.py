"""Authentication service.

Handles user registration and login. Uses bcrypt for password hashing.
JWT token generation is done at the route layer (this service is
framework-agnostic).
"""

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DBSession

from app.models.user import User
from app.errors import ValidationError, AuthenticationError, DuplicateError
from app.utils.validators import validate_username, validate_password


class AuthService:
    """User authentication business logic."""

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def register(self, username: str, password: str) -> User:
        """Register a new user and return the user object.

        Register does NOT log the user in automatically --
        the user must explicitly log in afterwards.
        (Per PRD-01: "注册后不自动登录")

        Args:
            username: Desired username (3-64 chars, alphanumeric/underscore/hyphen).
            password: Password (at least 8 characters, must contain letter + digit).

        Returns:
            The newly-created User instance.

        Raises:
            ValidationError: If username or password fail format checks.
            DuplicateError: If the username is already taken.
        """
        # Validate inputs
        cleaned_username = validate_username(username)
        validate_password(password)

        # Check for existing user with same username
        stmt = select(User).where(User.username == cleaned_username)
        existing = self.db.scalar(stmt)
        if existing is not None:
            raise DuplicateError("用户名已存在")

        # Create user
        user = User(username=cleaned_username)
        user.set_password(password)
        self.db.add(user)
        try:
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            raise DuplicateError("用户名已存在")

        return user

    def login(self, username: str, password: str) -> User:
        """Authenticate a user and return the user object.

        JWT token generation is handled by the route layer.
        Service layer stays framework-agnostic.

        Args:
            username: The user's username.
            password: The user's plain-text password.

        Returns:
            The authenticated User instance.

        Raises:
            AuthenticationError: If credentials are invalid.
        """
        # Query user by username (validate_username strips + validates)
        cleaned_username = validate_username(username)
        stmt = select(User).where(User.username == cleaned_username)
        user = self.db.scalar(stmt)

        if user is None:
            raise AuthenticationError("用户名或密码错误")

        # Verify password
        if not user.check_password(password):
            raise AuthenticationError("用户名或密码错误")

        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        """Fetch a user by their UUID.

        Args:
            user_id: The user's UUID string.

        Returns:
            User instance or None if not found.

        Raises:
            ValidationError: If user_id is not a valid UUID.
        """
        try:
            uuid.UUID(user_id)
        except (ValueError, AttributeError):
            return None
        return self.db.get(User, user_id)
