"""
Provide implementation of books repository.
"""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.external_services.database.models import Books
from src.repositories.base import PostgresRepository
from src.repositories.errors import IsbnBatchIsTooBigError
from src.structures.book import Book


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
        async with self._session() as session:
            query = select(Books).where(Books.isbn == isbn)
            result = (await session.execute(query)).one_or_none()

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

        async with self._session() as session:
            query = select(Books).where(Books.isbn.in_(isbn_batch))
            results = (await session.execute(query)).all()

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

    async def upsert_book_batch(self, books: list[Book]) -> None:
        """
        Upsert book batch.

        Args:
            books: list of Book objects.
        """
        stmt = insert(Books)
        stmt.on_conflict_do_update(
            index_elements=['isbn'],
            set_={
                Books.title.key: stmt.excluded.title,
                Books.author.key: stmt.excluded.author,
                Books.publisher_raw.key: stmt.excluded.publisher,
                Books.publisher.key: stmt.excluded.publisher,
                Books.url.key: stmt.excluded.url,
                Books.status.key: stmt.excluded.status,
                Books.genres.key: stmt.excluded.genres,
                Books.genres_raw.key: stmt.excluded.genres_raw,
            }
        )
        async with self._session() as session:
            await session.execute(stmt, [book.model_dump(mode='json') for book in books])
            await session.commit()
