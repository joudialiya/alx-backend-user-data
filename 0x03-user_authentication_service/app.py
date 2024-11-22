#!/usr/bin/env python3
"""Flask app module
"""
from flask import jsonify, Flask, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """Say hi"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Register a user"""
    email = request.form["email"]
    password = request.form["password"]
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Login method"""
    email = request.form["email"]
    password = request.form["password"]
    if not AUTH.valid_login(email, password):
        abort(401)
    response = jsonify({"email": email, "message": "logged in"})
    session_id = AUTH.create_session(email)
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
