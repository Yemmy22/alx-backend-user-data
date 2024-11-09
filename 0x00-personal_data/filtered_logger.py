#!/usr/bin/env python3
"""
A main function module
"""

import os
import mysql.connector
from datetime import datetime
import logging
from typing import List


# Set up basic logging configuration
logging.basicConfig(
        level=logging.INFO,
        format='[HOLBERTON] user_data INFO %(asctime)s: %(message)s'
        )
logger = logging.getLogger("user_data")


def get_db():
    """Creates and returns a connector to the database."""
    db = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return db


def filter_data(row: dict, fields: List[str]) -> str:
    """Filters sensitive data in a row."""
    filtered = []

    for key, value in row.items():
        if key in fields:
            filtered.append(f"{key}=***")
        else:
            filtered.append(f"{key}={value}")
    return "; ".join(filtered)


def main():
    """Main function to retrieve and log filtered user data."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    sensitive_fields = ["name", "email", "phone", "ssn", "password"]

    for row in cursor:
        filtered_row = filter_data(row, sensitive_fields)
        logger.info(filtered_row)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
