#!/usr/bin/env python3
"""
A flask app module
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

# Instantiate the Auth class to interact with the authentication logic
AUTH = Auth()

# Create a Flask application instance
app = Flask(__name__)


# Define a route for the root URL
@app.route('/')
def hello_world():
    return jsonify(message="Bienvenue")


# Define a route for the user registration (POST /users)
@app.route('/users', methods=['POST'])
def register_user() -> str:
    # Get email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')
    """
    if not email or not password:
        # If email or password are not provided, return a 400 error
        return jsonify({"message": "email and password are required"}
        ), 400
    """
    try:
        # Attempt to register the user using Auth.register_user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except Exception:
        # If the user already exists, catch the exception
        # and return a 400 error
        return jsonify({"message": "email already registered"}), 400


# Define a route for user login (POST /sessions)
@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Handles user login and creates a session."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)  # Respond with 401 Unauthorized if credentials are missing

    if not AUTH.valid_login(email, password):
        abort(401)  # Respond with 401 Unauthorized if credentials are invalid

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)  # Respond with 401 Unauthorized if session creation fails

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)  # Set session ID as a cookie
    return response


# Define a route for user logout (DELETE /sessions)
@app.route('/sessions', methods=['DELETE'])
def logout_user() -> str:
    """
    Logout a user by destroying their session.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)  # No session_id provided

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)  # Invalid session_id or no user found

    # Destroy the session
    AUTH.destroy_session(user.id)

    # Redirect the user to the home page
    return redirect("/")


# Define a route for user profile (GET /profile)
@app.route('/profile', methods=['GET'])
def user_profile() -> str:
    """
    Retrieve the profile of the logged-in user based on session_id.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Handle POST /reset_password endpoint to generate a reset token.
    """
    # Retrieve email from the form data
    email = request.form.get('email')

    if not email:
        abort(400, description="Email field is required")

    try:
        # Generate the reset token using Auth.get_reset_password_token
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # Respond with 403 if the email is not registered
        abort(403, description="Invalid email address")

    # Respond with the email and reset token
    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
