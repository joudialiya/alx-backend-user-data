#!/usr/bin/env python3
""" auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth manager class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Simply return false"""
        return False

    def authorization_header(self, request=None) -> str:
        """extract credentials"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """REtuns curent user"""
        return None
