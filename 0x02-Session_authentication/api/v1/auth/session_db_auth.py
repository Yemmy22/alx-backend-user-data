#!/usr/bin/env python3
"""
A SessionDBAuth Module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session authentication with database storage."""

    def create_session(self, user_id=None):
        """Create and store a session in the database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save to the database-like file
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the User ID by session ID from the database."""
        if not session_id:
            return None  # Return None if session_id is None

        # Search for UserSession by session_id
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            # Return None if no UserSession is found
            return None

        user_session = user_sessions[0]  # Assume session_id is unique
        if self.session_duration <= 0:
            return user_session.user_id  # No expiration

        # Check session expiration
        from datetime import datetime, timedelta
        created_at = user_session.created_at
        if not created_at:
            return None
        if datetime.now() > created_at + timedelta(
                seconds=self.session_duration
                ):
            return None  # Session expired

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy a session by removing it from the database."""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()  # Delete from the database
        return True
