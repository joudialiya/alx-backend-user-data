#!/usr/bin/env python3
"""Utilty module personal data"""
import logging
from typing import List
import re
import csv


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """A function tah maske fields"""
    for field in fields:
        message = re.sub(
            f"{field}=(.*?)*{separator}",
            f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """class constructor"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """oerload the format method"""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_logger() -> logging.Logger:
    """Returns a users info logger"""

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    handler.setLevel(logging.INFO)
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger
