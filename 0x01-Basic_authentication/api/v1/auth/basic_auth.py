#!/usr/bin/env python3
"""
A basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        Extracts the Base64 part from the Authorization header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Decodes the Base64 authorization header into a UTF-8 string.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 string and return it as a UTF-8 string
            decoded_value = base64.b64decode(base64_authorization_header)
            return decoded_value.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extracts user email and password from the
        decoded Base64 string.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # Split the string by the colon and return the two parts
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        Retrieves the User instance based on user email and password.
        """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        try:
            # Search for the user in the database
            users = User.search({"email": user_email})
            if not users or users == []:  # If no user found
                return None

            for user in users:
                # Check if the password is valid
                if user.is_valid_password(user_pwd):
                    return user
                return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current User instance based on the
        request authorization header. Returns the User instance
        if valid credentials are provided, None otherwise.
        """
        # Step 1: Extract the authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Step 2: Extract the base64-encoded authorization header
        base64_auth_header = self.extract_base64_authorization_header(
                auth_header
                )
        if base64_auth_header is None:
            return None
        string = self.decode_base64_authorization_header(
                base64_auth_header
                )
        if string is not None:
            # Step 3: Decode the base64 header to get the user credentials
            user_email, user_pwd = self.extract_user_credentials(
                    string
                    )
        if user_email is None or user_pwd is None:
            return None

        # Step 4: Retrieve the User object using the credentials
        user = self.user_object_from_credentials(
                user_email,
                user_pwd
                )
        return user
