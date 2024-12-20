#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """uuid wraper"""
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """Hash password"""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode("utf-8"),
                user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Create a user session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Map session to user"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int):
        """Destroy session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass
