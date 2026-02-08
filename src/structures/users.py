"""
Provide structures for users.
"""

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from src.enums.book import BookGenre


class User(BaseModel):
    """
    User model class.
    """
    id: int
    subscribed_genres: list[int] = Field(default_factory=list)
    subscribed_publishers: list[int] = Field(default_factory=list)
    subscribed_authors: list[str] = Field(default_factory=list)
