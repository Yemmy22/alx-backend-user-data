#!/usr/bin/env python3
"""
Module to create a logger with sensitive data redaction.
"""

import logging
from typing import List

# Define fields that are considered PII and should be redacted in logs
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for sensitive information
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the class
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redacts sensitive information in the log record's message.
        """
        original_message = super().format(record)
        return filter_datum(
                self.fields,
                self.REDACTION,
                original_message,
                self.SEPARATOR
                )


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Replaces the values of sensitive fields in
    a log message with a redaction string.
    """
    for field in fields:
        message = re.sub(
                fr"{field}=[^;]+",
                f"{field}={redaction}",
                message
                )
    return message


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
