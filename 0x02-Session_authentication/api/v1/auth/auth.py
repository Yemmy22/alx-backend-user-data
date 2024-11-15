#!/usr/bin/env python3
"""
Auth class module manages API authentication.
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Auth class for handling API authentication methods.
    """

    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
            ) -> bool:
        """
        Determines if authentication is required for a given path.
        """
        if path is None:
            return True
        if not excluded_paths or excluded_paths == []:
            return True

        # Ensure the path ends with a slash for comparison
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            # Check if the excluded path ends with '*' (wildcard)
            if excluded_path.endswith('*'):
                # Remove the '*' and compare if the
                # normalized path starts with the excluded prefix
                if normalized_path.startswith(excluded_path[:-1]):
                    # No authentication required for matching path
                    return False

            if normalized_path == excluded_path:
                return False

        return True

    def authorization_header(
            self,
            request=None
            ) -> str:
        """
        Returns the authorization header from the request.
        """
        if request is None:
            return None
        # Check if the Authorization header exists in the request
        header = request.headers.get('Authorization')
        if header is None:
            return None

        return header

    def current_user(
            self,
            request=None
            ) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the value of a session cookie from the request.
        """
        if request is None:
            return None

        # Get the cookie name from the environment variable
        session_name = getenv("SESSION_NAME")

        # Return the cookie value using .get() if session_name is defined
        return request.cookies.get(
                session_name
                ) if session_name else None
