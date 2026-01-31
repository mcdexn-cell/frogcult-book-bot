"""
Provide bot service implementation.
"""

from src.enums.book import GENRE_TO_CATEGORY_MAP
from src.repositories.users import UsersRepository
from src.structures.genre import GenreUserContext
from src.structures.publisher import PublisherUserContext
from src.utils.extractors.service import PhraseExtractionService


class BookBotService:
    """
    Book bot service implementation.
    """
    def __init__(self, users_repository: UsersRepository, publisher_extractor: PhraseExtractionService) -> None:
        """
        Initialize the service.

        Args:
            users_repository: users repository instance.
        """
        self._users_repository = users_repository
        self._publisher_extractor = publisher_extractor

    async def register(self, user_id: int) -> None:
        """
        Register a new user.

        Args:
            user_id: user id.
        """
        await self._users_repository.register(user_id=user_id)

    async def list_genres_for_user(self, user_id: int) -> list[GenreUserContext]:
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

    async def search_publishers_for_user(self, user_id: int, input_text: str) -> list[PublisherUserContext]:
        """
        Search for publishers in the input text given.

        Args:
            user_id: user id.
            input_text: input text.

        Returns:
            list of matched publishers.
        """
        user_data = await self._users_repository.get_user_by_id(user_id=user_id)
        matched_publishers =  self._publisher_extractor.extract_phrases(text=input_text)

        prepared_publishers: list[PublisherUserContext] = []
        for publisher in matched_publishers:
            is_subscribed = publisher in set(user_data.subscribed_publishers)
            publisher_data = PublisherUserContext(publisher=publisher, is_subscribed=is_subscribed)
            prepared_publishers.append(publisher_data)

        return prepared_publishers

    async def toggle_publisher_subscription(self, user_id: int, publisher: str, is_subscribed: bool) -> None:
        """
        Toggle publisher subscription in database.

        Args:
            user_id: user ID to toggle.
            publisher: publisher name to toggle.
            is_subscribed: is user already subscribed to the publisher.
        """
        await self._users_repository.toggle_publisher_subscription(
            user_id=user_id,
            publisher=publisher,
            is_subscribed=is_subscribed,
        )
