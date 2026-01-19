"""
Provide enums for scraper.
"""

from enum import StrEnum


class ParseMode(StrEnum):
    """
    Parse mode.
    """
    ONE = "one"
    ALL = "all"
