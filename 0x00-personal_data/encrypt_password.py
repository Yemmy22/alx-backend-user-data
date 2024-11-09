#!/usr/bin/env python3
"""
A hash_password module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt,
    returning a salted, hashed password in bytes.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
