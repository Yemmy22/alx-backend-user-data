#!/usr/bin/env python3
"""
An Auth class module.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a new UUID string.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes the object
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.
        """
        # Check if the user already exists
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Hash the password
            hashed_password = _hash_password(password)
            # Create the user and save to the database
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)

            # Compare the provided password with the stored hashed password
            return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                    )
        except NoResultFound:
            # If the user does not exist, return False
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a new session for a user by their email.
        """
        try:
            # Find the user corresponding to the given email
            user = self._db.find_user_by(email=email)

            # Generate a new UUID using the standalone _generate_uuid function
            session_id = _generate_uuid()

            # Update the user's session_id in the database
            self._db.update_user(user.id, session_id=session_id)

            # Return the generated session ID
            return session_id

        except NoResultFound:
            # Return None if the user is not found
            return None
