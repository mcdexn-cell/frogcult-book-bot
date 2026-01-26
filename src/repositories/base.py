"""
Provide base repository implementation.
"""

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)


class BaseRepository:
    """
    Base repository implementation.
    """


class PostgresRepository(BaseRepository):
    """
    Postgres repository class implementation.
    """

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        """
        Construct the object.

        Args:
            session: database session instance.
        """
        self._session = session
