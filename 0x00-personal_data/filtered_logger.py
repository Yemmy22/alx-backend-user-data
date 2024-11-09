#!/usr/bin/env python3
"""
Module for obfuscating specified fields in log messages
"""

import re
from typing import List


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
