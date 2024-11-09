#!/usr/bin/env python3
"""
Module for custom logging formatter with data redaction.
"""

import logging
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Redacts specified fields in a log message.

    Args:
        fields: List of fields to redact.
        redaction: String to replace field values.
        message: The log message.
        separator: Separator character between fields.

    Returns:
        The redacted log message.
    """
    pattern = '|'.join([f'{field}=[^;{separator}]*' for field in fields])
    return re.sub(
            pattern,
            lambda match: f"{match.group().split('=')[0]}={redaction}",
            message
            )


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
