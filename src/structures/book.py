"""
Provide structures for book.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from src.enums.book import BookStatus


@dataclass_json
@dataclass
class Book:
    """
    Book structure class.
    """
    title: str
    author: str
    publisher: str
    url: str
    status: BookStatus
    isbn: int
    genres: list[str]
