#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Import Auth based on the environment variable
auth = None
AUTH_TYPE = getenv('AUTH_TYPE')

if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == 'session_exp_auth':
    auth = SessionExpAuth()
elif AUTH_TYPE == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Handler executed before each request.
    Ensures that paths not excluded require valid authorization.
    """
    if auth is not None:
        excluded_paths = [
                '/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/',
                '/api/v1/auth_session/login/'
                ]
        # Check if the path requires authentication
        if auth.require_auth(request.path, excluded_paths):
            # If Authorization header is missing, abort with 401
            if auth.authorization_header(
                    request
                    ) is None and auth.session_cookie(request) is None:
                abort(401, description="Unauthorized")

            # If current user is None, abort with 403
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")
            request.current_user = auth.current_user(request)


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler for 403 Forbidden error.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handler for 401 Unauthorized error.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
