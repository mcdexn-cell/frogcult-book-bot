"""
Provide structures for genres.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pydantic import BaseModel

from src.enums.book import (
    BookGenre,
    BookGenreCategory,
)


@dataclass_json
@dataclass
class GenreUserContext:
    """
    Genre User context struct.
    """
    genre: BookGenre
    category: BookGenreCategory
    is_subscribed: bool


class GenreInDb(BaseModel):
    """
    Genre In DB struct.
    """
    id: int
    name: BookGenre
    category: BookGenreCategory
    mapping: list[str]
