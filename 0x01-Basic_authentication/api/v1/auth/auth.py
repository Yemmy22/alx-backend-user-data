#!/usr/bin/env python3
"""
Auth class module manages API authentication.
"""

from flask import request
from typing import List, TypeVar


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
            # Check if normalized path matches any excluded path
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
        return request.headers.get('Authorization', None)

    def current_user(
            self,
            request=None
            ) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.
        """
        return None
