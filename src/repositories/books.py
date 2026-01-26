"""
Provide implementation of books repository.
"""

from sqlalchemy import select

from src.enums.book import STATUS_REWRITE_RULES
from src.external_services.database.models import Books
from src.repositories.base import PostgresRepository
from src.repositories.errors import IsbnBatchIsTooBigError
from src.structures.book import (
    Book,
    BookStatus, BookAlert,
)


MAX_ISBN_RESULTS = 100


class BooksRepository(PostgresRepository):
    """
    Provide implementation of books repository.
    """

    async def get_by_isbn(self, isbn: int) -> Book | None:
        """
        Get book by isbn.

        Args:
            isbn: ISBN as integer.

        Returns:
            Book object.
        """
        with self._session() as session:
            query = select(Books).where(Books.isbn == isbn)
            result = await (session.execute(query)).one_or_none()

        if not result:
            return None

        return Book(
            title=result.title,
            author=result.author,
            isbn=result.isbn,
            genres=result.genres,
            genres_raw=result.genres_raw,
            publisher=result.publisher,
            publisher_raw=result.publisher_raw,
            url=result.url,
            status=result.status,
        )

    async def get_by_isbn_batch(self, isbn_batch: list[int]) -> list[Book] | None:
        """
        Get books by ISBN batch. Limited by 100 records.

        Args:
            isbn_batch: list of ISBNs as integers.

        Returns:
            list of Book objects.
        """
        if len(isbn_batch) > MAX_ISBN_RESULTS:
            raise IsbnBatchIsTooBigError

        with self._session() as session:
            query = select(Books).where(Books.isbn.in_(isbn_batch))
            results = await (session.execute(query)).all()

        prepared_results = []
        for result in results:
            Book(
                title=result.title,
                author=result.author,
                isbn=result.isbn,
                genres=result.genres,
                genres_raw=result.genres_raw,
                publisher=result.publisher,
                publisher_raw=result.publisher_raw,
                url=result.url,
                status=result.status,
            )
            prepared_results.append(result)

        return prepared_results

    async def _prepare_upsert_data(self, books: list[Book], write_alerts: bool = True) -> list[Book]:
        """
        Prepare upsert data for books.

        Args:
            books: list of Book objects.
            write_alerts: whether to write alerts to database.

        Returns:
            prepared list of Book objects.
        """
        alerts = []

        existing_books = await self.get_by_isbn_batch(isbn_batch=[book.isbn for book in books])
        existing_books_by_isbn = {book.isbn: book for book in existing_books}

        prepared_data = []
        for book in books:
            existing_book = existing_books_by_isbn.get(book.isbn)
            if not existing_book:
                prepared_data.append(book)
                alerts.append(BookAlert(isbn=book.isbn, status_after=book.status))
                continue

            if existing_book.status in STATUS_REWRITE_RULES.get(book.status, []):
                prepared_data.append(book)
                alerts.append(BookAlert(isbn=book.isbn, status_before=existing_book.status, status_after=book.status))

            if existing_book.genres and book.genres and existing_book.genres != book.genres:
                combined_genres = list(set(existing_book.genres + book.genres))
                existing_book.genres = combined_genres
                prepared_data.append(existing_book)

        if alerts and write_alerts:
            await self.write_alerts(alerts=alerts)

        return prepared_data

    async def upsert_book_batch(self, books: list[Book], write_alerts: bool = True) -> None:
        """
        Upsert book batch.

        Args:
            books: list of Book objects.
            write_alerts: whether to write alerts to database.
        """
        pass
