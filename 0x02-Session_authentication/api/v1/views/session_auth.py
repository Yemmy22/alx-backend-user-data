#!/usr/bin/env python3
"""
A Session authentication routes Module
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    POST /api/v1/auth_session/login
    Handles user login with session authentication.
    """
    # Retrieve email and password from request
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session ID for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Set the session ID in a cookie
    session_name = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def logout():
    """
    Handles session logout
    """
    if not auth.destroy_session(request):
        abort(404)  # If session destruction fails, return 404 error
    return jsonify({}), 200  # Successful logout returns an empty JSON
