"""
Provide bot service implementation.
"""

from src.enums.book import GENRE_TO_CATEGORY_MAP
from src.repositories.users import UsersRepository
from src.structures.genre import GenreUserContext


class BookBotService:
    """
    Book bot service implementation.
    """
    def __init__(self, users_repository: UsersRepository) -> None:
        """
        Initialize the service.

        Args:
            users_repository: users repository instance.
        """
        self._users_repository = users_repository

    async def register(self, user_id: int) -> None:
        """
        Register a new user.

        Args:
            user_id: user id.
        """
        await self._users_repository.register(user_id=user_id)

    async def list_genres(self, user_id: int) -> list[GenreUserContext]:
        """
        List all genres for user.

        Args:
            user_id: user id.

        Returns:
            list of genres.
        """
        user_data = await self._users_repository.get_user_by_id(user_id=user_id)

        prepared_genres: list[GenreUserContext] = []
        for genre, category in GENRE_TO_CATEGORY_MAP.items():
            prepared_genre = GenreUserContext(
                genre=genre,
                category=category,
                is_subscribed=genre in user_data.subscribed_genres,
            )
            prepared_genres.append(prepared_genre)

        return prepared_genres
