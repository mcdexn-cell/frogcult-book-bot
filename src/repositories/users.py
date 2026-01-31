"""
Provide users repository implementation.
"""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.external_services.database.models import Users
from src.repositories.base import PostgresRepository
from src.structures.users import User


class UsersRepository(PostgresRepository):
    """
    Users repository implementation.
    """

    async def register(self, user_id: int) -> None:
        """
        Register a new user.

        Args:
            user_id: user ID.
        """
        async with self._session() as session:
            stmt = insert(Users).values(id=user_id)
            stmt = stmt.on_conflict_do_nothing(index_elements=[Users.id])
            await session.execute(stmt)

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Get a user by ID.

        Args:
            user_id: user ID to get.

        Returns:
            User object.
        """
        stmt = select(Users).where(Users.id == user_id)
        async with self._session() as session:
            user = (await session.execute(stmt)).scalar_one_or_none()

        if not user:
            return None

        return User(
            id=user.id,
            subscribed_genres=user.subscribed_genres,
            subscribed_publishers=user.subscribed_publishers,
            subscribed_authors=user.subscribed_authors,
        )
