#!/usr/bin/env python3
"""
A collection of modules
"""
import logging
from typing import List
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


"""
Module for obfuscating specified fields in log messages
"""


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Obfuscates specified fields in a log message

    Args:
        fields: List of fields to obfuscate.
        redaction: String used to replace field values.
        message: Original log line.
        separator: Separator used between fields in the log line.

    Returns:
        A new log line with specified fields obfuscated
    """
    pattern = '|'.join([f'{field}=[^;{separator}]*' for field in fields])
    return re.sub(
            pattern,
            lambda match: f"{match.group().split('=')[0]}={redaction}",
            message
            )


"""
Module for custom logging formatter with data redaction.
"""


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter with fields for redaction.

        Args:
            fields: List of fields that should be redacted in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by redacting specified fields.

        Args:
            record: LogRecord instance.

        Returns:
            The formatted log record with specified fields redacted.
        """
        record.msg = filter_datum(
                self.fields, self.REDACTION,
                record.getMessage(),
                self.SEPARATOR
                )
        return super(RedactingFormatter, self).format(record)


"""
Module to create a logger with sensitive data redaction.
"""


def get_logger() -> logging.Logger:
    """
    Creates a logger configured to redact PII in log messages.

    Returns:
        logging.Logger: A logger configured with RedactingFormatter.
    """
    # Initialize the logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent propagation to other loggers

    # Create a StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # Attach the handler to the logger
    logger.addHandler(stream_handler)

    return logger


"""
Module to connect to a secure database.
"""


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
    db = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the MySQL database
    connection = MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db
    )

    return connection
