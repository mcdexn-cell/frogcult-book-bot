"""
Provide enums for book.
"""

from enum import StrEnum


class BookStatus(StrEnum):
    PREORDER = 'preorder'
    COMING_SOON = 'coming_soon'
    NEW = 'new'
