#!/usr/bin/env python3
""" auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session Manager"""
    def __init__(self):
        super().__init__()

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_onject = UserSession(
            user_id=user_id,
            session_id=session_id,
        )
        session_onject.save()

    def user_id_for_session_id(self, session_id=None):
        """Return user from session id"""
        if not session_id or type(session_id) is not str:
            return None
        session_object: UserSession = UserSession.get(session_id)
        if not session_object:
            return None
        if self.session_duration <= 0:
            return session_object.user_id
        created_at: datetime = session_object.updated_at
        if not created_at:
            return None
        if (created_at +
                timedelta(seconds=self.session_duration)
                < datetime.now()):
            return None
        return session_object.user_id

    def destroy_session(self, request=None):
        """Destroy session"""
        if not request:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        session_object: UserSession = UserSession.get(cookie)
        session_object.remove()
        return True
