"""
Provide structures for parser.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from src.enums.scraper import ParseMode


@dataclass_json
@dataclass
class ParserFieldConfig:
    """
    Parser field.
    """
    selector: str
    attribute: str | None = None
    regex: str | None = None
    regex_index: int = 0
    mode: ParseMode = ParseMode.ONE
