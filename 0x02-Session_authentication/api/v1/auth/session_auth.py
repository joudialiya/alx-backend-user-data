#!/usr/bin/env python3
""" auth module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session Manager class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create settion"""
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def destroy_session(self, request=None):
        """destroy a session"""
        if not request:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        SessionAuth.user_id_by_session_id.pop(cookie)
        return True

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user id"""
        if not session_id or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Create user"""
        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)
        user = User.get(user_id)
        return user
