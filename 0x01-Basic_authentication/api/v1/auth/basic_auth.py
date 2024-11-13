#!/usr/bin/env python3
"""
A basic auth module
"""
from api.v1.auth.auth import Auth
import base64


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
