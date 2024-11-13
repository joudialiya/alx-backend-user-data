#!/usr/bin/env python3
""" auth module
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session experation auth"""
    def __init__(self):
        """claass constructor"""
        potential = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(potential)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        SessionAuth.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user from session id"""
        if not session_id or type(session_id) is not str:
            return None
        session_object = SessionAuth.user_id_by_session_id.get(session_id)
        if not session_object:
            return None
        if self.session_duration <= 0:
            return session_object.get("user_id")
        created_at: datetime = session_object.get("created_at")
        if not created_at:
            return None
        if (created_at +
                timedelta(seconds=self.session_duration)
                < datetime.now()):
            return None
        return session_object.get("user_id")
