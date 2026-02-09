"""
Provide dependencies for services.
"""

from src.bot.service import BookBotService
from src.dependencies.repositories import (
    get_books_repository,
    get_genres_repository,
    get_publishers_repository,
    get_users_repository,
)
from src.utils.extractors.service import PhraseExtractionService


async def get_book_bot_service():
    """
    Get book bot service.
    """
    publishers_repository = get_publishers_repository()
    publishers_mapping = await publishers_repository.get_publisher_id_to_mapping()
    publisher_extractor = PhraseExtractionService(phrases_mapping=publishers_mapping)
    return BookBotService(
        books_repository=get_books_repository(),
        users_repository=get_users_repository(),
        genres_repository=get_genres_repository(),
        publishers_repository=publishers_repository,
        publisher_extractor=publisher_extractor,
    )
