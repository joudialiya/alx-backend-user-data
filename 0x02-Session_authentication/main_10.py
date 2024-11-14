#!/usr/bin/env python3
""" Main 0
"""

from models.user import User

user = User()
user.email = "root"
user.password = "toor"
user.save()