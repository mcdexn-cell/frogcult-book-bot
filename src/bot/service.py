"""
Provide bot service implementation.
"""

from src.enums.book import GENRE_TO_CATEGORY_MAP
from src.repositories.publishers import PublishersRepository
from src.repositories.users import UsersRepository
from src.structures.genre import GenreUserContext
from src.structures.publisher import PublisherUserContext, PublisherInDb
from src.utils.extractors.service import PhraseExtractionService


class BookBotService:
    """
    Book bot service implementation.
    """
    def __init__(
            self,
            users_repository: UsersRepository,
            publisher_extractor: PhraseExtractionService,
            publishers_repository: PublishersRepository,
    ) -> None:
        """
        Initialize the service.

        Args:
            users_repository: users repository instance.
        """
        self._users_repository = users_repository
        self._publisher_extractor = publisher_extractor
        self._publishers_repository = publishers_repository

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
        matched_publisher_ids = self._publisher_extractor.extract_phrases(text=input_text)

        publishers_data = await self._publishers_repository.get_publishers_by_ids(ids=matched_publisher_ids)

        prepared_publishers: list[PublisherUserContext] = []
        for publisher in publishers_data:
            is_subscribed = publisher.id in set(user_data.subscribed_publishers)
            publisher_data = PublisherUserContext(
                id=publisher.id,
                name=publisher.name,
                is_subscribed=is_subscribed,
            )
            prepared_publishers.append(publisher_data)

        return prepared_publishers

    async def toggle_publisher_subscription(self, user_id: int, publisher_id: int, is_subscribed: bool) -> None:
        """
        Toggle publisher subscription in database.

        Args:
            user_id: user ID to toggle.
            publisher_id: publisher ID to toggle.
            is_subscribed: is user already subscribed to the publisher.
        """
        await self._users_repository.toggle_publisher_subscription(
            user_id=user_id,
            publisher_id=publisher_id,
            is_subscribed=is_subscribed,
        )
