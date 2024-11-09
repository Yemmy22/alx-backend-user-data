#!/usr/bin/env python3
"""
A is_valid function module.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt,
    returning a salted, hashed password in bytes.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: The hashed password with salt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if a provided password matches the hashed password.
    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plaintext password to validate.
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
