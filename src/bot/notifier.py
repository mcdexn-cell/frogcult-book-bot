"""
Provide bot notifier service.
"""

from asyncio import Semaphore

from aiogram_broadcaster import Broadcaster

from src.bot.markup.books import get_book_notification_message
from src.repositories.users import UsersRepository
from src.structures.book import Book


class BookBotNotifierService:
    """
    Boot bot notifier service.
    """

    def __init__(self, broadcaster: Broadcaster, users_repository: UsersRepository, semaphore: Semaphore | None = None):
        """
        Construct the object.

        Args:
            broadcaster: telegram bot broadcaster instance.
            users_repository: users repository instance.
        """
        self._broadcaster = broadcaster
        self._users_repository = users_repository
        self._semaphore = semaphore or Semaphore(10)

    async def notify_book_subscribers(self, book: Book) -> None:
        """
        Notify subscribers of requested book.

        Args:
            book: book instance.
        """
        async with self._semaphore:
            message_content = get_book_notification_message(book=book)

            async for user_id_batch in self._users_repository.iter_subscribed_user_ids_batches(
                    publisher_id=book.publisher_id,
                    author=book.author,
                    genre_ids=book.genre_ids,
                ):
                mailer = await self._broadcaster.create_mailer(
                    content=message_content,
                    chats=user_id_batch,
                )
                await mailer.start()
