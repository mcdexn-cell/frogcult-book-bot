"""
Provide dependencies for services.
"""

from src.bot.service import BookBotService
from src.dependencies.repositories import get_users_repository


def get_book_bot_service():
    """
    Get book bot service.
    """
    return BookBotService(users_repository=get_users_repository())
