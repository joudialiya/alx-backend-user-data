#!/usr/bin/env python3
"""Utilty module"""
import logging
import re


"""
Write a function called filter_datum that returns the log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character
is separating all fields in the log line (message)
"""


def filter_datum(fields, redaction, message, separator):
    """A function tah maske fields"""
    for field in fields:
        message = re.sub(
            "{}=[^ {}]*{}".format(field, *[separator]*2),
            "{}={}{}".format(field, redaction, separator),
            message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg, self.SEPARATOR)
        return super().format(record)
