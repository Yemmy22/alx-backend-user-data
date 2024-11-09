#!/usr/bin/env python3
"""
Module to connect to a secure database.
"""


import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


def get_db() -> MySQLConnection:
    """
    Connects to the MySQL database using
    credentials from environment variables.

    Returns:
        MySQLConnection: A connection object to the database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connection
