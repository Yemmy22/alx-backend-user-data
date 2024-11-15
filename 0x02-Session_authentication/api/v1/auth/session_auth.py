#!/usr/bin/env python3
"""
A Session Authentication Module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        Args:
            user_id (str): The user ID to associate with the session.
        Returns:
            str: The created Session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique Session ID
        session_id = str(uuid4())

        # Store the user_id by session_id
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a User ID based on a Session ID.
        Args:
            session_id (str): The Session ID to lookup.
        Returns:
            str: The User ID associated with the Session ID,
            or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the User ID using the session_id
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Return a User instance based on a cookie value.

        Uses:
        - self.session_cookie() to extract the session ID from the request
        - self.user_id_for_session_id() to retrieve the user ID
        - User.get() to fetch the User instance
        """
        if request is None:
            return None

        # Extract session ID from request cookie
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Retrieve user ID from session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Fetch and return the User instance
        return User.get(user_id)
