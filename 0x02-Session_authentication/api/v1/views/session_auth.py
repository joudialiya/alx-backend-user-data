#!/usr/bin/env python3
""" Module of session based auth view
"""
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify
import os


@app_views.route(
    "/auth_session/login",
    methods=["POST"],
    strict_slashes=False)
def login():
    """Login logic"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or email == '':
        return {"error": "email missing"}, 400
    if not password or password == '':
        return {"error": "password missing"}, 400
    try:
        users = User.search({"email": email})
    except Exception:
        return {"error": "no user found for this email"}, 404
    if len(users) <= 0:
        return {"error": "no user found for this email"}, 404
    user: User = users[0]
    if not user.is_valid_password(password):
        return {"error": "wrong password"}, 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(
        os.getenv("SESSION_NAME", "_my_session_id"),
        session_id)
    return response
