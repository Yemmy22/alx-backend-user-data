#!/usr/bin/env python3
"""
Auth class module manages API authentication
"""


from flask import request, Request
from typing import List, TypeVar, Optional


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
            request: Optional[Request] = None
            ) -> Optional[str]:
        """
        Returns the authorization header from the request.
        """
        return None

    def current_user(
            self,
            request: Optional[Request] = None
            ) -> Optional[TypeVar('User')]:
        """
        Retrieves the current user based on the request.
        """
        return None
