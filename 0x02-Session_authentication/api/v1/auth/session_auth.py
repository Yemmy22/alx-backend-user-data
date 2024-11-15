#!/usr/bin/env python3
"""
A Session Authentication Module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
