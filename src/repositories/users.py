"""
Provide users repository implementation.
"""

from sqlalchemy import (
    select,
    update,
)
from sqlalchemy.dialects.postgresql import insert

from src.database.models import Users
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
            await session.commit()

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
            subscribed_genres=user.subscribed_genres or [],
            subscribed_publishers=user.subscribed_publishers or [],
            subscribed_authors=user.subscribed_authors or [],
        )

    async def toggle_publisher_subscription(self, user_id: int, publisher_id: int, is_subscribed: bool) -> None:
        """
        Toggle publisher subscription in database.

        Args:
            user_id: user ID to toggle.
            publisher_id: publisher ID to toggle.
            is_subscribed: is user already subscribed to the publisher.
        """
        user_data = await self.get_user_by_id(user_id)

        if is_subscribed:
            user_data.subscribed_publishers.remove(publisher_id)

        else:
            user_data.subscribed_publishers.append(publisher_id)

        stmt = update(Users).where(Users.id == user_id).values(subscribed_publishers=user_data.subscribed_publishers)
        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

    async def toggle_genre_subscription(self, user_id: int, genre_id: int, is_subscribed: bool) -> None:
        """
        Toggle genre subscription in database.

        Args:
            user_id: user ID to toggle.
            genre_id: genre ID to toggle.
            is_subscribed: is user already subscribed to the genre.
        """
        user_data = await self.get_user_by_id(user_id)

        if is_subscribed:
            user_data.subscribed_genres.remove(genre_id)

        else:
            user_data.subscribed_genres.append(genre_id)

        stmt = update(Users).where(Users.id == user_id).values(subscribed_genres=user_data.subscribed_genres)
        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()
