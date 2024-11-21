#!/usr/bin/env python3
"""
A test script for the user authentication service.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Test registering a user."""
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users", data=payload)
    assert response.status_code == 200, f"Expected 200, got\
            {response.status_code}"
    assert response.json() == {
            "email": email,
            "message": "user created"
            }, f"Unexpected payload: {response.json()}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with a wrong password."""
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=payload)
    assert response.status_code == 401, f"Expected 401, got\
            {response.status_code}"


def log_in(email: str, password: str) -> str:
    """Test logging in with correct credentials."""
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=payload)
    assert response.status_code == 200, f"Expected 200, got\
            {response.status_code}"
    assert "session_id" in response.cookies, "session_id not in cookies"
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Test accessing the profile endpoint while not logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected 403, got\
            {response.status_code}"


def profile_logged(session_id: str) -> None:
    """Test accessing the profile endpoint while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got\
            {response.status_code}"


def log_out(session_id: str) -> None:
    """Test logging out."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got\
            {response.status_code}"


def reset_password_token(email: str) -> str:
    """Test generating a reset password token."""
    payload = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=payload)
    assert response.status_code == 200, f"Expected 200, got\
            {response.status_code}"
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating the password."""
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    response = requests.put(f"{BASE_URL}/reset_password", data=payload)
    assert response.status_code == 200, f"Expected 200, got\
            {response.status_code}"
    assert response.json() == {
            "email": email,
            "message": "Password updated"
            }, f"Unexpected payload: {response.json()}"


# Testing the application
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
