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
        return False

    def authorization_header(
            self,
            request=None
            ) -> str:
        """
        Returns the authorization header from the request.
        """
        return None

    def current_user(
            self,
            request=None
            ) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.
        """
        return None
