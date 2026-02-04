"""
Provide implementation of books repository.
"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert

from src.database.models import (
    Books,
    Genres,
    books_genres,
)
from src.repositories.base import PostgresRepository
from src.repositories.errors import IsbnBatchIsTooBigError
from src.structures.book import (
    Book,
    BookGenresRecord,
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
        async with self._session() as session:
            query = select(Books).options(joinedload(Books.genres)).where(Books.isbn == isbn)
            result = (await session.execute(query)).unique().one_or_none()

        if not result:
            return None

        return Book(
            title=result.title,
            author=result.author,
            isbn=result.isbn,
            genres=result.genres,
            genres_raw=result.genres_raw,
            publisher=result.publisher,
            publisher_id=result.publisher_id,
            url=result.url,
            status=result.status,
            source=result.source,
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
            query = (
                select(Books).options(joinedload(Books.genres)).where(Books.isbn.in_(isbn_batch))
            )
            results = (await session.execute(query)).unique().scalars().all()

        prepared_results = []
        for result in results:
            prepared_result = Book(
                title=result.title,
                author=result.author,
                isbn=result.isbn,
                source=result.source,
                genres=[genre.name for genre in result.genres],
                genre_ids=[genre.id for genre in result.genres],
                genres_raw=result.genres_raw,
                publisher=result.publisher,
                publisher_id=result.publisher_id,
                url=result.url,
                status=result.status,
            )
            prepared_results.append(prepared_result)

        return prepared_results

    async def upsert_book_batch(self, books: list[Book]) -> None:
        """
        Upsert book batch.

        Args:
            books: list of Book objects.
        """
        stmt = insert(Books)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Books.isbn],
            set_={
                Books.title.key: stmt.excluded.title,
                Books.author.key: stmt.excluded.author,
                Books.source.key: stmt.excluded.source,
                Books.publisher_id.key: stmt.excluded.publisher_id,
                Books.publisher.key: stmt.excluded.publisher,
                Books.url.key: stmt.excluded.url,
                Books.status.key: stmt.excluded.status,
                Books.genres_raw.key: stmt.excluded.genres_raw,
            }
        )
        async with self._session() as session:
            await session.execute(stmt, [book.model_dump(mode='json') for book in books])
            await session.commit()

        book_genres_records: list[BookGenresRecord] = []
        for book in books:
            if not book.genre_ids:
                continue

            for genre_id in book.genre_ids:
                book_genres_records.append(BookGenresRecord(book_isbn=book.isbn, genre_id=genre_id))

        if book_genres_records:
            await self.upsert_book_genres_batch(book_genres=book_genres_records)

    async def upsert_book_genres_batch(self, book_genres: list[BookGenresRecord]) -> None:
        """
        Upsert book genres batch.

        Args:
            book_genres: list of BookGenresRecord objects.
        """
        stmt = insert(books_genres)
        stmt = stmt.on_conflict_do_nothing()

        async with self._session() as session:
            await session.execute(stmt, [record.model_dump(mode='json') for record in book_genres])
            await session.commit()
