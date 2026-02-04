"""
Provide structures for publishers.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pydantic import BaseModel


@dataclass_json
@dataclass
class PublisherUserContext:
    """
    Publisher User context struct.
    """
    publisher: str
    is_subscribed: bool


class PublisherInDb(BaseModel):
    """
    Publisher In DB struct.
    """
    id: int
    name: str
    mapping: list[str]
