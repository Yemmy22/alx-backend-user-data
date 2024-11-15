#!/usr/bin/env python3
"""A Session Expiration Module"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Authentication with expiration."""

    def __init__(self):
        """Initialize the session duration."""
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with an expiration date."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a user ID only if the session is valid."""
        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get("created_at")
        if not created_at:
            return None

        if created_at + timedelta(
                seconds=self.session_duration
                ) < datetime.now():
            return None

        return session_data.get("user_id")
