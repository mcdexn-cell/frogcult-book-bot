"""
Scraper class implementation.
"""

from collections import deque
from typing import Any

from src.enums.book import STATUS_REWRITE_RULES
from src.repositories.books import BooksRepository
from src.scraper.book.factory import BookScraperFactory
from src.scraper.config import PublisherConfig
from src.scraper.engine import PlaywrightScraperEngine
from src.scraper.publisher.factory import PublisherScraperFactory
from src.settings import settings
from src.structures.book import Book, BookAlert


class MainScraper:
    """
    Main scraper class.
    """

    def __init__(
            self,
            books_repository: BooksRepository,
            scraper_engine: PlaywrightScraperEngine,
            book_scraper_params: dict[str, Any],
    ) -> None:
        """
        Construct the object.

        Args:
            books_repository: books repository instance.
            scraper_engine: scraper engine instance.
        """
        self._books_repository = books_repository
        self._scraper_engine = scraper_engine
        self._book_scraper_params = book_scraper_params

    async def _handle_alerts(self, alerts: list[BookAlert]):
        """
        Process found book alerts.
        """
        pass

    async def _process_book_batch(self, books: list[Book], handle_alerts: bool) -> None:
        """
        Process book batch.
        """
        alerts = []

        existing_books = await self._books_repository.get_by_isbn_batch(isbn_batch=[book.isbn for book in books])
        existing_books_by_isbn = {book.isbn: book for book in existing_books}

        prepared_books = []
        for book in books:
            existing_book = existing_books_by_isbn.get(book.isbn)
            if not existing_book:
                prepared_books.append(book)
                alerts.append(BookAlert(isbn=book.isbn, status_after=book.status))
                continue

            if existing_book.status in STATUS_REWRITE_RULES.get(book.status, []):
                prepared_books.append(book)
                alerts.append(BookAlert(isbn=book.isbn, status_before=existing_book.status, status_after=book.status))

            if existing_book.genres and book.genres and existing_book.genres != book.genres:
                combined_genres = list(set(existing_book.genres + book.genres))
                existing_book.genres = combined_genres
                prepared_books.append(existing_book)

        if alerts and handle_alerts:
            await self._handle_alerts(alerts=alerts)

        if prepared_books:
            print(prepared_books)
            await self._books_repository.upsert_book_batch(books=prepared_books)

    async def run_with_config(self, config: list[PublisherConfig], handle_alerts: bool) -> None:
        """
        Run scraper with config.

        Args:
            config: list of publisher config.
            handle_alerts: whether to handle book alerts.
        """
        book_batch = deque(maxlen=settings.scraper.book_batch_size)

        for publisher_config in config:
            book_scraper = BookScraperFactory.get(
                publisher_name=publisher_config.name,
                scraper_engine=self._scraper_engine,
                **self._book_scraper_params,
            )
            publisher_scraper = PublisherScraperFactory.get(
                publisher_name=publisher_config.name,
                config=publisher_config,
                scraper_engine=self._scraper_engine,
                book_scraper=book_scraper
            )

            async for book in publisher_scraper.iter_scrape_books_batches():
                book_batch.extend(book)

                if len(book_batch) >= book_batch.maxlen:
                    await self._process_book_batch(books=book_batch, handle_alerts=handle_alerts)
                    book_batch.clear()

            if book_batch:
                await self._process_book_batch(books=book_batch, handle_alerts=handle_alerts)
