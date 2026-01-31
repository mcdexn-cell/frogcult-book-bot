"""
Provide structures for book.
"""

from pydantic import BaseModel

from src.enums.book import BookStatus, BookGenre


class Book(BaseModel):
    """
    Book structure class.
    """
    title: str
    author: str
    source: str
    publisher_raw: str
    url: str
    status: BookStatus
    isbn: int
    genres_raw: list[str]
    publisher: str | None = None
    genres: list[BookGenre] | None = None


class BookAlert(BaseModel):
    """
    Book alert structure class.
    """
    isbn: int
    status_before: BookStatus | None = None
    status_after: BookStatus | None = None
