"""
Provide dependencies for repositories.
"""

from src.dependencies.database import get_session
from src.repositories.users import UsersRepository


def get_users_repository():
    """
    Get users repository.
    """
    return UsersRepository(session=get_session())
