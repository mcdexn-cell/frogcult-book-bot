"""
Provide dependencies for repositories.
"""

from src.dependencies.database import get_session
from src.repositories.books import BooksRepository
from src.repositories.genres import GenresRepository
from src.repositories.publishers import PublishersRepository
from src.repositories.users import UsersRepository


def get_users_repository():
    """
    Get users repository.
    """
    return UsersRepository(session=get_session())


def get_publishers_repository():
    """
    Get publishers repository.
    """
    return PublishersRepository(session=get_session())


def get_genres_repository():
    """
    Get genres repository.
    """
    return GenresRepository(session=get_session())


def get_books_repository():
    """
    Get books repository.
    """
    return BooksRepository(session=get_session())
