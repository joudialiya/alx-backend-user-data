#!/usr/bin/env python3
""" auth module
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """Auth manager class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Simply return false"""
        if not path:
            return True
        if not excluded_paths:
            return True
        if path[-1] != "/":
            path += "/"
        for excluded_path in excluded_paths:
            if re.match(excluded_path, path):
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """extract credentials"""
        if not request:
            return None
        header = request.headers.get("Authorization")
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """REtuns curent user"""
        return None
