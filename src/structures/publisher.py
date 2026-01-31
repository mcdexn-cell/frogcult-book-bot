"""
Provide structures for publishers.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PublisherUserContext:
    """
    Publisher User context struct.
    """
    publisher: str
    is_subscribed: bool
