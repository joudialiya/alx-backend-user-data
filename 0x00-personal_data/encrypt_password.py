#!/usr/bin/env python3
"""Utilty module encript passwords"""
import bcrypt


def hash_password(password: str) -> str:
    """Hashing the password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate a password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
