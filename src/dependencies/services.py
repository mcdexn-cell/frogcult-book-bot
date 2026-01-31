"""
Provide dependencies for services.
"""

from src.bot.service import BookBotService
from src.dependencies.repositories import get_users_repository
from src.utils.extractors.mappings import PUBLISHERS_MAPPING
from src.utils.extractors.service import PhraseExtractionService


def get_book_bot_service():
    """
    Get book bot service.
    """
    publisher_extractor = PhraseExtractionService(phrases_mapping=PUBLISHERS_MAPPING)
    return BookBotService(users_repository=get_users_repository(), publisher_extractor=publisher_extractor)
