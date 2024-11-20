#!/usr/bin/env python3
"""
An Auth class module.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.
        """
        # Check if the user already exists
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass  # No user found, proceed with registration

        # Hash the password
        hashed_password = self._hash_password(password)

        # Create the user and save to the database
        new_user = self._db.add_user(email, hashed_password)

        return new_user
