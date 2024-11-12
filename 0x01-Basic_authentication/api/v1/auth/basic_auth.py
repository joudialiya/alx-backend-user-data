#!/usr/bin/env python3
""" auth module
"""
from flask import request
from typing import List, TypeVar, Tuple
import base64
import re
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic auth handler"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extract the crdentials part"""
        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        matches = re.match(r"Basic (.*)", authorization_header)
        if not matches:
            return None
        return matches.groups()[0]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode the credentials part"""
        if type(base64_authorization_header) is not str:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return (base64
                    .b64decode(base64_authorization_header)
                    .decode("utf-8"))
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extract the credentials in a pain way"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        matches = re.match(
            r"(.*):(.*)",
            decoded_base64_authorization_header)
        if not matches:
            return (None, None)
        return matches.groups()

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Create user object"""
        if not user_email and type(user_email) != str:
            return None
        if not user_pwd and type(user_pwd) != str:
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        user: User = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user"""
        header = self.authorization_header(request)
        credentails_part = self.extract_base64_authorization_header(header)
        email, password = self.extract_user_credentials(
            self.decode_base64_authorization_header(credentails_part)
        )
        return self.user_object_from_credentials(email, password)
